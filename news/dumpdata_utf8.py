"""Скрипт для выгрузки данных из БД, где используются русские символы."""
import os
import django
from django.core.management import call_command

# Установите переменную окружения DJANGO_SETTINGS_MODULE для вашего проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

# Инициализируйте Django
django.setup()

output_file = 'mydata.json'
# Выгрузите только статьи и категории
with open(output_file, 'w', encoding='utf-8') as file:
    call_command('dumpdata', 'simp_dungeon.Post', 'simp_dungeon.Category', indent=4, stdout=file)
