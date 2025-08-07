from django.core.management.base import BaseCommand
import requests
from requests.exceptions import RequestException
from locations.models import State, City

class Command(BaseCommand):
    help = 'Import states from API de localidades'
    
    def handle(self, *args, **options):
        self.import_states()
        self.import_cities()
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

    def import_cities(self):
        states = State.objects.all()

        total_inserted, total_updated = 0, 0

        for state in states:
            url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{state.id}/municipios'
            try:
                data = requests.get(url).json()
            except RequestException as e:
                self.stderr.write(f'[EXCEPTION - CITIES] FAILED to request data State {state.name}: {e}')
                continue

            inserted, updated = 0, 0

            for city in data:
                obj, created = City.objects.update_or_create(
                    id=city['id'],
                    defaults={
                        'name': city['nome'],
                        'state': state
                    }
                )
                if created:
                    inserted += 1
                else:
                    updated += 1

            self.stdout.write(f'[CITIES - {state.acronym}] Inserted: {inserted}, Updated: {updated}')
            total_inserted += inserted
            total_updated += updated
            
        self.stdout.write(self.style.SUCCESS(
            f'[CITY - TOTAL] Inserted: {total_inserted}, Updated: {total_updated}'
        ))