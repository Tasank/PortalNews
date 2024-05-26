from django.apps import AppConfig


class SimpDungeonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simp_dungeon'

    # Чтобы изменения учитывались импортируем файл с сигналами
    def ready(self):
        import signals
