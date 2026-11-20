from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import json


class BlogPost(models.Model):
    """Blog post model for essays and articles"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    excerpt = models.TextField(max_length=300, help_text="Short summary for listings")
    read_time = models.IntegerField(help_text="Estimated read time in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    featured_image = models.FileField(upload_to='blog/', blank=True, null=True)  # Use ImageField when Pillow is installed
    category = models.ForeignKey(
        'BlogCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts'
    )
    order = models.PositiveSmallIntegerField(default=0, help_text="Position within its category")
    article_nodes = models.CharField(
        max_length=500,
        blank=True,
        default='',
        help_text='Węzły grafu wiedzy do podświetlenia (ID oddzielone przecinkami, np. "mindset, persistence, dweck")'
    )

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})


class BlogCategory(models.Model):
    """Categories for blog posts"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0, help_text="Display order on the blog page")

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class GraphNode(models.Model):
    """Knowledge graph node - represents a term, concept, or researcher"""
    KIND_CHOICES = [
        ('term', 'Termin kursu'),
        ('concept', 'Pojęcie pomocnicze'),
        ('person', 'Badacz'),
    ]

    WEEK_CHOICES = [
        (1, 'Tydzień 1 - Fundamenty'),
        (2, 'Tydzień 2 - Pamięć'),
        (3, 'Tydzień 3 - Przetwarzanie'),
        (4, 'Tydzień 4 - Praktyka'),
    ]

    node_id = models.CharField(
        max_length=50,
        primary_key=True,
        verbose_name='ID węzła',
        help_text='Unikalny identyfikator węzła (np. "mindset", "test", "dweck")'
    )
    label = models.CharField(
        max_length=200,
        verbose_name='Nazwa',
        help_text='Pełna nazwa węzła wyświetlana na grafie'
    )
    kind = models.CharField(
        max_length=10,
        choices=KIND_CHOICES,
        verbose_name='Typ węzła'
    )
    day = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Dzień',
        help_text='Dzień w kursie (opcjonalnie dla badaczy)'
    )
    week = models.PositiveSmallIntegerField(
        choices=WEEK_CHOICES,
        verbose_name='Tydzień'
    )
    summary = models.TextField(
        verbose_name='Podsumowanie',
        help_text='Krótki opis pojęcia'
    )
    example = models.TextField(
        blank=True,
        verbose_name='Przykład',
        help_text='Opcjonalny przykład użycia'
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Kolejność',
        help_text='Kolejność wyświetlania w panelu administracyjnym'
    )

    class Meta:
        ordering = ['week', 'day', 'kind', 'order']
        verbose_name = 'Węzeł grafu'
        verbose_name_plural = 'Węzły grafu'

    def __str__(self):
        return f"{self.label} ({self.node_id})"


class GraphEdge(models.Model):
    """Knowledge graph edge - represents a relationship between two nodes"""
    BASIS_CHOICES = [
        ('stated', 'Podane w kursie'),
        ('inferred', 'Wnioskowane'),
    ]

    source = models.ForeignKey(
        GraphNode,
        on_delete=models.CASCADE,
        related_name='outgoing_edges',
        verbose_name='Węzeł źródłowy'
    )
    target = models.ForeignKey(
        GraphNode,
        on_delete=models.CASCADE,
        related_name='incoming_edges',
        verbose_name='Węzeł docelowy'
    )
    relation = models.CharField(
        max_length=100,
        verbose_name='Relacja',
        help_text='Etykieta relacji (np. "przewiduje", "koryguje", "autor")'
    )
    basis = models.CharField(
        max_length=10,
        choices=BASIS_CHOICES,
        default='stated',
        verbose_name='Podstawa'
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Kolejność',
        help_text='Kolejność wyświetlania w panelu administracyjnym'
    )

    class Meta:
        ordering = ['source', 'order']
        verbose_name = 'Krawędź grafu'
        verbose_name_plural = 'Krawędzie grafu'
        unique_together = ['source', 'target', 'relation']

    def __str__(self):
        return f"{self.source.node_id} → {self.relation} → {self.target.node_id}"
