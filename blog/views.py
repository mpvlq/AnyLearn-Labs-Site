from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import BlogPost, BlogCategory, GraphNode, GraphEdge


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


def graph_data(request):
    """Return knowledge graph data as JSON"""
    nodes = GraphNode.objects.all()
    edges = GraphEdge.objects.select_related('source', 'target').all()

    data = {
        'nodes': [
            {
                'id': node.node_id,
                'label': node.label,
                'kind': node.kind,
                'day': node.day,
                'week': node.week,
                'summary': node.summary,
                'example': node.example,
            }
            for node in nodes
        ],
        'edges': [
            {
                'source': edge.source.node_id,
                'relation': edge.relation,
                'target': edge.target.node_id,
                'basis': edge.basis,
            }
            for edge in edges
        ]
    }

    return JsonResponse(data)
