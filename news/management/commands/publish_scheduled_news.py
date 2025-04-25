from django.core.management.base import BaseCommand
from news.models import News
from django.utils import timezone

class Command(BaseCommand):
    help = 'Publica automaticamente notícias agendadas para publicação'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        scheduled_news = News.objects.filter(
            status='draft',
            scheduled_pub_date__lte=now
        )

        for news in scheduled_news:
            news.status = 'published'
            news.pub_date = now
            news.save()
            self.stdout.write(self.style.SUCCESS(f'Notícia publicada: {news.title}'))

        if not scheduled_news.exists():
            self.stdout.write(self.style.WARNING('Nenhuma notícia agendada para publicar.'))
