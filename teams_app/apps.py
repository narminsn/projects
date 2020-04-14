from django.apps import AppConfig


class TeamsAppConfig(AppConfig):
    name = 'teams_app'
    def ready(self):
        import teams_app.signals
