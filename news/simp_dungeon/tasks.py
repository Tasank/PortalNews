from datetime import datetime
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import News, Category
from .signals import send_notifications
from NewsApp import settings


@shared_task
def send_post_for_subscribers_celery(post_pk):
    post = News.objects.get(id=post_pk)
    categories = post.category.all()
    subscribers_all = []
    for category in categories:
        subscribers_all += category.subscribe.all()
    subscribers_list = {}
    for person in subscribers_all:
        subscribers_list[person.username] = person.email
    for n in subscribers_list.items():
        send_notifications(n[0], post.title, post.text[:50], n[1], post.pk)


@shared_task
def weekly_post():
    today = datetime.datetime.now()
    day_week_ago = today - datetime.timedelta(days=7)
    posts = News.objects.filter(date_post__gte=day_week_ago)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribe__email', flat=True))

    html_content = render_to_string(
        'post_created_email.html',
        {
            'posts': posts,
            'link': f'{settings.SITE_URL}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новости за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()