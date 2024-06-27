from django.core.management.base import BaseCommand, CommandError
from simp_dungeon.models import Post, Category


class Command(BaseCommand):
    help = 'Удалить все новости/статьи в категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Удалить все статьи в категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(Title=options['category'])
            Post.objects.filter(category=category).delete()
            # в случае неправильного подтверждения говорим, что в доступе отказано
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.Title}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {category.Title}'))