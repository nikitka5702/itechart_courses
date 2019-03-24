from django.core.management.base import BaseCommand
from app.models import Shop, Department, Item


class Command(BaseCommand):
    help = 'Clears tables of app'

    def handle(self, *args, **options):
        for model in [Shop, Department, Item]:
            model.objects.all().delete()
            self.stdout.write(f'Dumped table {model.__name__}')
