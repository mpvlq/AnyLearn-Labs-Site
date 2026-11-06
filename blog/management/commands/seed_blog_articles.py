from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from blog.models import BlogCategory, BlogPost


# Article index from design/blog_page/AnyLearn Blog.dc.html: (category, [(title, excerpt), ...])
ARTICLES = [
    ('Fundamenty', [
        ('Uczenie się pod własną kontrolą', 'Co znaczy samodzielnie kierować własną nauką i od czego zacząć.'),
        ('Samoregulowane uczenie się', 'Planowanie, monitorowanie i ocena — trzy fazy, które porządkują naukę.'),
        ('Metapoznanie', 'Myślenie o własnym myśleniu: jak zauważyć, że czegoś jeszcze nie rozumiesz.'),
        ('Nastawienie na rozwój i na stałość', 'Jak przekonania o własnych zdolnościach wpływają na wysiłek i wytrwałość.'),
        ('Motywacja wewnętrzna i zewnętrzna', 'Skąd bierze się chęć do nauki i dlaczego nagrody nie zawsze pomagają.'),
    ]),
    ('Pamięć', [
        ('Efekt testowania', 'Przywoływanie z pamięci utrwala wiedzę skuteczniej niż ponowne czytanie.'),
        ('Efekt odstępu', 'Dlaczego nauka rozłożona w czasie wygrywa z nauką na ostatnią chwilę.'),
        ('Pożądane trudności', 'Trudności, które spowalniają naukę dziś, a wzmacniają ją na dłużej.'),
        ('Iluzja kompetencji', 'Kiedy materiał wydaje się znajomy, choć nie potrafisz go odtworzyć.'),
        ('Krzywa zapominania', 'Jak szybko tracimy nową wiedzę i co możemy z tym zrobić.'),
    ]),
    ('Przetwarzanie', [
        ('Pytania elaboracyjne', 'Pytanie „dlaczego?” wiąże nowe fakty z tym, co już wiesz.'),
        ('Teoria podwójnego kodowania', 'Słowo i obraz razem zapamiętujemy lepiej niż każde z osobna.'),
        ('Efekt generowania', 'To, co sami wytworzymy, pamiętamy lepiej niż to, co przeczytamy.'),
        ('Przeplatanie materiału', 'Mieszanie typów zadań uczy rozpoznawać, której metody użyć.'),
        ('Teoria obciążenia poznawczego', 'Pamięć robocza ma granice — jak projektować naukę, by ich nie przekraczać.'),
    ]),
    ('Praktyka', [
        ('Celowa praktyka', 'Ćwiczenie na granicy możliwości, z jasnym celem i szybką informacją zwrotną.'),
        ('Sądy o uczeniu się i kalibracja', 'Jak trafnie oceniać, co już umiesz, a czego jeszcze nie.'),
        ('Teoria wyznaczania celów', 'Konkretne i ambitne cele prowadzą do lepszych wyników niż „postaraj się”.'),
        ('Transfer wiedzy', 'Jak sprawić, by to, czego się nauczysz, działało także w nowych sytuacjach.'),
        ('Samokontrola i odroczona gratyfikacja', 'Strategie, które pomagają wybrać naukę zamiast natychmiastowej przyjemności.'),
    ]),
]


class Command(BaseCommand):
    help = 'Create the blog categories and article stubs from the blog design'

    def handle(self, *args, **options):
        author = User.objects.filter(is_superuser=True).first()
        if author is None:
            self.stderr.write('No superuser found. Run createsuperuser or populate_sample_data first.')
            return

        for cat_order, (category_name, articles) in enumerate(ARTICLES, start=1):
            category, _ = BlogCategory.objects.update_or_create(
                slug=slugify(category_name),
                defaults={'name': category_name, 'order': cat_order},
            )
            for post_order, (title, excerpt) in enumerate(articles, start=1):
                post, created = BlogPost.objects.get_or_create(
                    slug=slugify(title),
                    defaults={
                        'title': title,
                        'author': author,
                        'excerpt': excerpt,
                        'content': excerpt,
                        'read_time': 6,
                        'published_at': timezone.now(),
                        'is_published': True,
                    },
                )
                post.category = category
                post.order = post_order
                post.save(update_fields=['category', 'order'])
                if created:
                    self.stdout.write(f'Created article: {title}')

        self.stdout.write(self.style.SUCCESS('Blog articles seeded.'))
