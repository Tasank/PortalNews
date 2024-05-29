from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from django.conf import settings
from .models import Category

# Отправка сообщений
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title, # Заголовок
        body='', # Тело пустое т.к. используем шаблон
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers, # Кому отправляем
    )
    # Добавляем к сообщению наш шаблон
    msg.attach_alternative(html_content, 'text/html')

@receiver(m2m_changed, sender=Category)
def notify_about_new_post(sender, instance, subscribers, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers += cat.subscribers.all()
            subscribers_emails += [a.email for a in subscribers] # Добавление почт подписчиков

        send_notifications(instance.preview(),instance.pk, instance.title, subscribers_emails)