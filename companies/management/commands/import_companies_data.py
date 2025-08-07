from django.core.management.base import BaseCommand
from companies.services.import_companies import import_companies

class Command(BaseCommand):
    help = 'Import datas from an extern file'

    def add_arguments(self, parser):
        parser.add_argument('zip_path', type=str, help='Path to file')

    def handle(self, *args, **kwargs):
        path = kwargs['zip_path']
        import_companies(path)
