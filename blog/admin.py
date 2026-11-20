from django.contrib import admin
from .models import BlogPost, BlogCategory


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order', 'author', 'published_at', 'read_time', 'is_published']
    list_editable = ['category', 'order']
    list_filter = ['is_published', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'excerpt', 'article_nodes']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ['-published_at']

    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('title', 'slug', 'author', 'category', 'order')
        }),
        ('Treść', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Graf wiedzy', {
            'fields': ('article_nodes',),
            'description': (
                'Węzły grafu wiedzy do podświetlenia w tym artykule. '
                'Podaj ID węzłów oddzielone przecinkami, np.: mindset, persistence, dweck. '
                '<br><br><strong>Dostępne węzły:</strong><br>'
                '<strong>Terminy:</strong> sdl, srl, meta, mindset, motiv, test, space, dd, illus, forget, ei, dual, gen, inter, clt, dp, jol, goal, transfer, td<br>'
                '<strong>Pojęcia:</strong> forethought, performance, selfref, self_control, meta_know, meta_reg, persistence, autonomy, competence, relatedness, overjust, fluency, prior_know, encoding, discrimination, working_mem, schema, intrinsic_load, extraneous_load, germane_load, feedback, mere_rep, dunning, mastery, perfgoal, near, far, hyperbolic, delayed_grat, impl_int, precommit<br>'
                '<strong>Badacze:</strong> knowles, grow, zimmerman, flavell, dweck, deci_ryan, roediger, ebbinghaus, cepeda, bjork, koriat, metcalfe, pressley, dunlosky, paivio, mayer, slamecka, rohrer, sweller, ericsson, locke, ames, elliot, thorndike, ainslie, mischel, gollwitzer'
            )
        }),
        ('Metadane', {
            'fields': ('read_time', 'published_at', 'is_published')
        }),
    )


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
