from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Course(models.Model):
    """Course model for self-paced learning courses"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Początkujący'),
        ('intermediate', 'Średniozaawansowany'),
        ('advanced', 'Zaawansowany'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, help_text="Brief description for course cards")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    lesson_count = models.IntegerField(default=0, help_text="Number of lessons in the course")
    estimated_hours = models.DecimalField(max_digits=4, decimal_places=1, help_text="Estimated completion time")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.FileField(upload_to='courses/thumbnails/', blank=True, null=True)  # Use ImageField when Pillow is installed
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'slug': self.slug})

    def get_modules_structure(self):
        """Group lessons into modules based on lesson metadata"""
        lessons = self.lessons.all().order_by('order')
        modules = []
        current_module = None

        for lesson in lessons:
            # Check if this lesson defines a new module
            if 'módulo' in lesson.title.lower() or 'module' in lesson.title.lower():
                # This is a module header
                if current_module:
                    modules.append(current_module)
                current_module = {
                    'title': lesson.title,
                    'description': lesson.content[:200] if lesson.content else '',
                    'lessons': []
                }
            elif current_module:
                # This is a lesson within the current module
                current_module['lessons'].append(lesson)

        # Add the last module
        if current_module:
            modules.append(current_module)

        # If no modules were found, create default structure
        if not modules:
            # Default: split lessons into 4 modules evenly
            lesson_list = list(lessons)
            module_count = min(4, len(lesson_list))
            lessons_per_module = len(lesson_list) // module_count if module_count > 0 else 0

            module_data = [
                {'title': 'Zbieranie materiałów', 'description': 'Przygotujesz źródła, z których notatnik będzie korzystał: własne notatki, materiały z wykładów i nagrania.'},
                {'title': 'Rozmowa z wiedzą', 'description': 'Nauczysz się zadawać pytania swoim materiałom, prosić o wyjaśnienia i porównywać źródła.'},
                {'title': 'Testowanie', 'description': 'Wykorzystasz notatnik do tworzenia pytań sprawdzających i fiszek na podstawie własnych źródeł.'},
                {'title': 'Sprawdzian', 'description': 'Końcowy test obejmujący materiał ze wszystkich modułów.'},
            ]

            for i in range(module_count):
                start_idx = i * lessons_per_module
                end_idx = start_idx + lessons_per_module if i < module_count - 1 else len(lesson_list)
                modules.append({
                    'title': module_data[i]['title'] if i < len(module_data) else f'Moduł {i+1}',
                    'description': module_data[i]['description'] if i < len(module_data) else '',
                    'lessons': lesson_list[start_idx:end_idx]
                })

        return modules


class Lesson(models.Model):
    """Individual lessons within a course"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    content = models.TextField()
    order = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=10, help_text="Estimated duration in minutes")
    is_free_preview = models.BooleanField(default=False, help_text="Available without enrollment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course', 'order']
        unique_together = ['course', 'slug']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Enrollment(models.Model):
    """Track user enrollments in courses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percentage = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class LessonProgress(models.Model):
    """Track user progress through individual lessons"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['enrollment', 'lesson']
        verbose_name_plural = 'Lesson Progress'

    def __str__(self):
        return f"{self.enrollment.user.username} - {self.lesson.title}"


class Newsletter(models.Model):
    """Newsletter subscription model"""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
