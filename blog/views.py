from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from .models import BlogPost, BlogCategory


def blog_list(request):
    """Article index grouped by category"""
    published = BlogPost.objects.filter(is_published=True).order_by('order', '-published_at')
    categories = [
        category
        for category in BlogCategory.objects.prefetch_related(
            Prefetch('posts', queryset=published, to_attr='published_posts')
        )
        if category.published_posts
    ]

    context = {
        'categories': categories,
    }
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    """Blog post detail page"""
    post = get_object_or_404(BlogPost.objects.select_related('category', 'author'), slug=slug, is_published=True)
    siblings = []
    if post.category:
        siblings = list(
            post.category.posts.filter(is_published=True).exclude(pk=post.pk).order_by('order')
        )

    context = {
        'post': post,
        'siblings': siblings,
    }
    return render(request, 'blog/blog_detail.html', context)
