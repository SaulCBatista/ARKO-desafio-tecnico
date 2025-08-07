from django.core.management.base import BaseCommand
import requests
from requests.exceptions import RequestException
from locations.models import State

class Command(BaseCommand):
    help = 'Import states from API de localidades'
    
    def handle(self, *args, **options):
        self.import_states()
        return 

    def import_states(self):
        url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
        try:
            data = requests.get(url).json()
        except RequestException as e: 
            self.stderr.write(f'[EXCEPTION - STATES] FAILED to request data: {e}')
            return
        
        inserted, updated = 0, 0

        for state in data:
            obj, created = State.objects.update_or_create(
                id=state['id'],
                defaults={
                    'name': state['nome'],
                    'acronym': state['sigla'],
                    'region': state['regiao']['nome'],
                }
            )

            if created:
                inserted += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'[STATES] Inserted: {inserted}, Updated: {updated}'
        ))