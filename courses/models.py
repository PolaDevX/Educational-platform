from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from checkout.models import Transaction

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    bio = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')

class Course(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(null=True)
    description = models.TextField()
    image = models.ImageField()
    price = models.FloatField()
    featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

class Cart(models.Model):
    session_id = models.CharField(max_length=255)
    items = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.session_id

class Order(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    courses = models.ManyToManyField('Course', blank=True)
    customer = models.JSONField(default=dict)
    total = models.FloatField()
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    @property
    def customer_name(self):
        if 'first_name' in self.customer:
            return f"{self.customer.get('first_name', '')} {self.customer.get('last_name', '')}".strip()
        elif 'name' in self.customer:
            return self.customer.get('name', '')
        elif 'full_name' in self.customer:
            return self.customer.get('full_name', '')
        return str(self.customer)

    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return f"{self.course.name} - {self.title}"


class Lesson(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='lessons/videos/', null=True, blank=True)
    content = models.TextField(null=True, blank=True) 
    is_preview = models.BooleanField(default=False) 
    order = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')

    def __str__(self):
        return self.title


class LessonComment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_comments')
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        if self.parent:
            return f"Reply by {self.user.username} on Comment #{self.parent.id}"
        return f"Comment by {self.user.username} on {self.lesson.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class AboutPageContent(models.Model):
    title = models.CharField(max_length=200, default="عن الموقع", verbose_name="عنوان الصفحة")
    description = models.TextField(verbose_name="من نحن؟")
    our_mission = models.TextField(verbose_name="هدفنا")
    what_we_offer = models.TextField(verbose_name="ماذا نقدم؟")

    class Meta:
            verbose_name = _('AboutPageContent')
            verbose_name_plural = _('About Page Contents')

    def __str__(self):
        return "إعدادات وتعديل صفحة عن الموقع"

class StudentReview(models.Model):
    about_page = models.ForeignKey(AboutPageContent, on_delete=models.CASCADE, related_name='reviews', verbose_name="صفحة عن الموقع")
    student_name = models.CharField(max_length=100, verbose_name="اسم الطالب")
    student_title = models.CharField(max_length=100, blank=True, null=True, verbose_name="الدولة")
    student_image = models.ImageField(upload_to='reviews/', null=True, blank=True, verbose_name="صورة الطالب")
    review_text = models.TextField(verbose_name="رأي الطالب")

    def __str__(self):
        return self.student_name