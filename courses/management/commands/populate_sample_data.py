from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from courses.models import Course, Lesson
from blog.models import BlogPost


class Command(BaseCommand):
    help = 'Populate database with sample courses and blog posts'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Get or create a user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@anylearn.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user (username: admin, password: admin123)'))

        # Create sample courses
        courses_data = [
            {
                'title': 'Foundations of Statistics',
                'short_description': 'Averages, spread and uncertainty, built up from small worked examples.',
                'description': 'Learn the fundamentals of statistics through practical examples and real-world applications. This course covers averages, standard deviation, probability, and statistical inference.',
                'difficulty': 'beginner',
                'lesson_count': 12,
                'estimated_hours': 8.0,
                'is_free': True,
                'is_published': True,
            },
            {
                'title': 'Writing Clear Technical Prose',
                'short_description': 'How to explain a system so the reader understands it on the first pass.',
                'description': 'Master the art of technical writing. Learn how to explain complex concepts clearly, structure your documents effectively, and write for your audience.',
                'difficulty': 'intermediate',
                'lesson_count': 9,
                'estimated_hours': 6.0,
                'price': 49.00,
                'is_free': False,
                'is_published': True,
            },
            {
                'title': 'Introduction to Machine Learning',
                'short_description': 'From a straight line through data to a small neural network you train yourself.',
                'description': 'Start your machine learning journey. Learn about linear regression, classification, neural networks, and train your first models using real datasets.',
                'difficulty': 'beginner',
                'lesson_count': 15,
                'estimated_hours': 12.0,
                'price': 79.00,
                'is_free': False,
                'is_published': True,
            },
        ]

        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={**course_data, 'instructor': user}
            )
            if created:
                self.stdout.write(f'Created course: {course.title}')

                # Add sample lessons
                for i in range(1, min(4, course.lesson_count + 1)):
                    Lesson.objects.create(
                        course=course,
                        title=f'Lesson {i}: Introduction to Core Concepts',
                        content=f'This is the content for lesson {i}. In this lesson, you will learn key concepts and practical applications.',
                        order=i,
                        duration_minutes=30 + (i * 5),
                        is_free_preview=(i == 1)
                    )
                self.stdout.write(f'  Added {min(3, course.lesson_count)} sample lessons')

        # Create sample blog posts
        blog_posts_data = [
            {
                'title': 'How spaced repetition actually works',
                'excerpt': 'Understanding the science behind one of the most effective learning techniques.',
                'content': '''Spaced repetition is a learning technique that involves reviewing information at increasing intervals.

The key insight is that our memory works best when we review information just before we're about to forget it. This creates stronger memory traces and leads to better long-term retention.

Research shows that spacing out your learning sessions is far more effective than cramming. By strategically timing your reviews, you can significantly improve your retention while spending less total time studying.

In this post, we'll explore the cognitive science behind spaced repetition and how you can apply it to your own learning.''',
                'read_time': 7,
                'published_at': timezone.now(),
                'is_published': True,
            },
            {
                'title': 'Why every course is a sequence of small problems',
                'excerpt': 'The learning science behind problem-based education.',
                'content': '''The most effective way to learn any skill is through solving progressively more challenging problems.

When you encounter a problem, your brain actively engages with the material. You're not just passively receiving information – you're testing hypotheses, making connections, and building mental models.

This is why every course on AnyLearn Labs is structured as a sequence of problems. Each problem builds on the previous one, gradually increasing in difficulty as your skills develop.

The result? Deeper understanding, better retention, and skills you can actually apply.''',
                'read_time': 5,
                'published_at': timezone.now(),
                'is_published': True,
            },
            {
                'title': 'Learning without a teacher: notes from a year of self-study',
                'excerpt': 'What I learned about learning on my own, without formal instruction.',
                'content': '''Self-directed learning is a superpower. But it requires a different approach than traditional classroom learning.

Over the past year, I've taught myself statistics, programming, and machine learning through self-study. Here are the key lessons I've learned:

1. **Structure is essential**: You need a clear path through the material, even without a teacher.
2. **Active learning beats passive reading**: Solve problems, build projects, teach others.
3. **Community matters**: Find others learning the same material.
4. **Patience with yourself**: Learning takes time, especially when you're figuring out the path yourself.

The good news? With the right resources and approach, you can learn almost anything on your own.''',
                'read_time': 11,
                'published_at': timezone.now(),
                'is_published': True,
            },
        ]

        for post_data in blog_posts_data:
            post, created = BlogPost.objects.get_or_create(
                title=post_data['title'],
                defaults={**post_data, 'author': user}
            )
            if created:
                self.stdout.write(f'Created blog post: {post.title}')

        self.stdout.write(self.style.SUCCESS('\nSample data created successfully!'))
        self.stdout.write('\nYou can now:')
        self.stdout.write('  - Visit the site at http://127.0.0.1:8000/')
        self.stdout.write('  - Log in to admin at http://127.0.0.1:8000/admin/')
        self.stdout.write('  - Username: admin')
        self.stdout.write('  - Password: admin123')
