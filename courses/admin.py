from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_per_page = 20

@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    list_per_page = 20

@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'is_preview', 'order']
    list_filter = ['section__course']
    search_fields = ['title']
    list_per_page = 20

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_select_related =  ['transaction']
    list_display = ['id', 'email', 'amount', 'payment_method', 'items', 'created_at']

    def amount(self, obj):
        if obj.transaction:
            return obj.transaction.amount
        return '-'

    def items(self, obj):
        if obj.transaction and obj.transaction.items:
            return len(obj.transaction.items)
        return '-'

    def email(self, obj):
        if obj.transaction:
            return obj.transaction.customer_email
        return '-'


    def payment_method(self, obj):
        if obj.transaction:
            return obj.transaction.get_payment_method_display()
        return '-'


    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

class StudentReviewInline(admin.TabularInline):
    model = models.StudentReview
    extra = 1

@admin.register(models.AboutPageContent)
class AboutPageAdmin(admin.ModelAdmin):
    inlines = [StudentReviewInline]
    list_per_page = 20

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)