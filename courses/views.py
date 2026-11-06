from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.http import url_has_allowed_host_and_scheme
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException
from .models import Course, Lesson, Enrollment, Newsletter
from .forms import ContactForm, NewsletterForm
from blog.models import BlogPost
import logging

logger = logging.getLogger(__name__)


def home(request):
    """Landing page with featured courses and blog posts"""
    featured_courses = Course.objects.filter(is_published=True)[:3]
    recent_blog_posts = BlogPost.objects.filter(is_published=True)[:3]

    context = {
        'courses': featured_courses,
        'blog_posts': recent_blog_posts,
    }
    return render(request, 'home.html', context)


def course_list(request):
    """List all available courses"""
    courses = Course.objects.filter(is_published=True)
    paginator = Paginator(courses, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'courses/course_list.html', context)


def course_detail(request, slug):
    """Course detail page with modules and lessons"""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    is_enrolled = False

    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    # Get modules structure from the Course model
    modules = course.get_modules_structure()

    context = {
        'course': course,
        'modules': modules,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def enroll_course(request, slug):
    """Enroll user in a course"""
    course = get_object_or_404(Course, slug=slug, is_published=True)

    if course.is_free:
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,
            course=course
        )
        if created:
            messages.success(request, f'Pomyślnie zapisałeś się na kurs {course.title}!')
        else:
            messages.info(request, 'Jesteś już zapisany na ten kurs.')
        return redirect('courses:course_detail', slug=course.slug)
    else:
        # Redirect to payment page (to be implemented)
        messages.info(request, 'Integracja płatności wkrótce dostępna!')
        return redirect('courses:course_detail', slug=course.slug)


def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            newsletter, created = Newsletter.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Dziękujemy za subskrypcję!')
            else:
                messages.info(request, 'Jesteś już zapisany do newslettera.')
        else:
            messages.error(request, 'Proszę podać prawidłowy adres email.')

        next_url = request.POST.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
    return redirect('courses:home')


def contact_form(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            try:
                subject = f'Nowa wiadomość kontaktowa od {name}'
                email_message = f'Od: {name}\nEmail: {email}\n\nWiadomość:\n{message}'

                send_mail(
                    subject,
                    email_message,
                    settings.EMAIL_HOST_USER,
                    [settings.CONTACT_FORM_RECIPIENT],
                    fail_silently=False,
                )
                messages.success(request, 'Dziękujemy za wiadomość! Odpowiemy najszybciej jak to możliwe.')
            except SMTPException as e:
                logger.error(f'Contact form email failed: {str(e)}')
                messages.error(request, 'Wystąpił błąd podczas wysyłania wiadomości. Proszę spróbować ponownie.')
        else:
            messages.error(request, 'Proszę wypełnić wszystkie pola formularza prawidłowo.')

    return redirect('courses:home')
