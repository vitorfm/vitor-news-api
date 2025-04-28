from django.core.mail import send_mail
from django.utils import timezone
from .models import News
from celery import shared_task


@shared_task
def send_notification_email(news_id, news_title):
    print(
        f"📬 Enviando notificação de publicação da notícia ID {news_id} - Título: {news_title}"
    )
    # Aqui no futuro poderia ser enviado um e-mail real
    return f"Notificação enviada para notícia {news_id}"


@shared_task
def send_real_email(recipient_email, news_title):
    subject = f"Nova notícia publicada: {news_title}"
    message = f'A notícia "{news_title}" foi publicada no Vitor News!'
    from_email = "noreply@vitornews.com"
    recipient_list = [recipient_email]

    send_mail(subject, message, from_email, recipient_list)
    print(f"📧 E-mail enviado para {recipient_email} sobre a notícia: {news_title}")


@shared_task
def publish_scheduled_news():
    """Publica automaticamente notícias agendadas que já passaram da hora."""
    now = timezone.now()
    # Seleciona notícias que estão em rascunho e a data de publicação agendada chegou
    news_to_publish = News.objects.filter(status="draft", scheduled_pub_date__lte=now)

    for news in news_to_publish:
        news.status = "published"
        news.pub_date = now
        news.save()
        print(f"✅ Notícia publicada automaticamente: {news.title}")

    if not news_to_publish.exists():
        print("ℹ️ Nenhuma notícia para publicar agora.")
