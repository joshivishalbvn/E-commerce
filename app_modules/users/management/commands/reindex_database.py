# myapp/management/commands/reindex_database.py

from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection

class Command(BaseCommand):
    help = 'Reindex all database tables and their indexes to improve performance'

    def handle(self, *args, **options):
        # Get all models from all installed apps
        all_models = apps.get_models()

        with connection.cursor() as cursor:
            for model in all_models:
                table_name = model._meta.db_table
                
                # Get index names for the current model
                index_names = [index.name for index in model._meta.indexes]

                # If there are indexes, reindex them
                if index_names:
                    for index_name in index_names:
                        try:
                            cursor.execute(f"REINDEX INDEX {index_name};")
                            self.stdout.write(self.style.SUCCESS(f'Successfully reindexed index {index_name} on table {table_name}.'))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'Error reindexing index {index_name} on table {table_name}: {e}'))
                else:
                    self.stdout.write(self.style.WARNING(f'No indexes found for table {table_name}.'))
