from django.apps import AppConfig
from django.core.management import call_command


class YourAppConfig(AppConfig):
    name = 'online_retail_app'

    def ready(self):
        call_command('seeddb', '--csv_file', 'path/to/default/csvfile.csv')
