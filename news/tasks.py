from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_notification_email(news_id, news_title):
    print(f"📬 Enviando notificação de publicação da notícia ID {news_id} - Título: {news_title}")
    # Aqui no futuro poderia ser enviado um e-mail real
    return f"Notificação enviada para notícia {news_id}"


@shared_task
def send_real_email(recipient_email, news_title):
    subject = f'Nova notícia publicada: {news_title}'
    message = f'A notícia "{news_title}" foi publicada no Vitor News!'
    from_email = 'noreply@vitornews.com'
    recipient_list = [recipient_email]

    send_mail(subject, message, from_email, recipient_list)
    print(f"📧 E-mail enviado para {recipient_email} sobre a notícia: {news_title}")

