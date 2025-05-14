from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Adds the Groups Teacher and Student to the database'

    def handle(self, *args, **options):
        groups = ['Teacher', 'Student']
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" was created.'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists.'))