from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان المقال")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="الكاتب")
    content = models.TextField(verbose_name="محتوى المقال")
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="صورة المقال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ النشر")

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return self.title