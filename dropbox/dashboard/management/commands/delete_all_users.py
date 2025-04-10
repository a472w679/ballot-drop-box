from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Deletes all user accounts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--include-superusers',
            action='store_true',
            help='Include superusers in deletion'
        )

    def handle(self, *args, **options):
        User = get_user_model()
        if options['include_superusers']:
            count, _ = User.objects.all().delete()
        else:
            count, _ = User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} users'))
