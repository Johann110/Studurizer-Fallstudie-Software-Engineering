from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Leere die django_migrations Tabelle'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM django_migrations;")
        connection.commit()
        self.stdout.write(self.style.SUCCESS('django_migrations Tabelle erfolgreich geleert'))