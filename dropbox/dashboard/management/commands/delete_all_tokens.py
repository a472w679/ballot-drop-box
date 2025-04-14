from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Deletes all authentication tokens'

    def handle(self, *args, **options):
        count, _ = Token.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} tokens'))
