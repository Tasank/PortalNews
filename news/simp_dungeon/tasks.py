from datetime import datetime, timedelta
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
from .signals import send_notifications
from news import settings


@shared_task
def send_post_for_subscribers_celery(post_pk):
    post = Post.objects.select_related('category').get(id=post_pk) #  select_related для уменьшения количества запросов
    # к базе данных: Это улучшит производительность запроса.
    categories = post.category.all()

    subscribers_emails = set() # Использование множества (set) для удаления дубликатов подписчиков.
    for category in categories:
        subscribers_emails.update(category.subscribe.values_list('email', flat=True))

    send_notifications(
        preview=post.text[:50],
        pk=post.pk,
        title=post.title,
        subscribers=list(subscribers_emails)
    )


@shared_task
def weekly_post():
    today = datetime.now()
    day_week_ago = today - timedelta(days=7)

    # Получаем все посты за последнюю неделю
    posts = Post.objects.filter(date_post__gte=day_week_ago)

    # Получаем уникальные категории из этих постов
    categories = posts.values_list('category__name', flat=True).distinct()

    # Получаем уникальные email подписчиков этих категорий
    subscribers = Category.objects.filter(name__in=categories).values_list('subscribe__email', flat=True).distinct()

    # Подготовка контента для email
    html_content = render_to_string(
        'post_created_email.html',
        {
            'posts': posts,
            'link': f'{settings.SITE_URL}'
        }
    )

    # Формирование и отправка email
    msg = EmailMultiAlternatives(
        subject='Новости за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
