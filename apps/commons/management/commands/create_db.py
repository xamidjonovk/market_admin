from django.core.management.base import BaseCommand
from django.db import connections, DEFAULT_DB_ALIAS
from psycopg2 import OperationalError, connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Command(BaseCommand):
    help = 'Creates the database for this project'

    def handle(self, *args, **options):
        db_settings = connections[DEFAULT_DB_ALIAS].settings_dict
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_pass = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings['PORT']

        # Connect to the default database (usually "postgres")
        try:
            conn = connect(dbname='postgres', user=db_user, password=db_pass, host=db_host, port=db_port)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            cursor.close()
            conn.close()
            self.stdout.write(self.style.SUCCESS(f'Successfully created database {db_name}'))
        except OperationalError as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
        except Exception as e:
            if 'already exists' in str(e):
                self.stdout.write(self.style.WARNING(f'Database {db_name} already exists'))
            else:
                raise
