from django.contrib import admin
from .models import Course, Lesson, Enrollment, LessonProgress, Newsletter


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ['title', 'order', 'duration_minutes', 'is_free_preview']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'lesson_count', 'price', 'is_free', 'is_published']
    list_filter = ['difficulty', 'is_free', 'is_published', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'instructor', 'difficulty')
        }),
        ('Content', {
            'fields': ('description', 'short_description', 'lesson_count', 'estimated_hours')
        }),
        ('Pricing', {
            'fields': ('price', 'is_free')
        }),
        ('Publishing', {
            'fields': ('is_published', 'thumbnail')
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration_minutes', 'is_free_preview']
    list_filter = ['course', 'is_free_preview']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'enrolled_at', 'progress_percentage', 'completed']
    list_filter = ['completed', 'enrolled_at']
    search_fields = ['user__username', 'course__title']
    readonly_fields = ['enrolled_at', 'completed_at']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'completed', 'last_accessed']
    list_filter = ['completed', 'last_accessed']
    search_fields = ['enrollment__user__username', 'lesson__title']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
