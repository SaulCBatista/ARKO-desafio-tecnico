# locations/management/commands/import_ibge.py
from django.core.management.base import BaseCommand
from locations.services import import_locations


class Command(BaseCommand):
    help = 'Import states, cities and districts from IBGE API'

    def handle(self, *args, **options):
        # States
        states_result = import_locations.import_states()
        if 'error' in states_result:
            self.stderr.write(states_result['error'])
        else:
            self.stdout.write(self.style.SUCCESS(
                f"[STATES] Inserted: {states_result['inserted']}, Updated: {states_result['updated']}"
            ))

        # Cities
        cities_result = import_locations.import_cities()
        self.stdout.write(self.style.SUCCESS(
            f"[CITIES - TOTAL] Inserted: {cities_result['inserted']}, Updated: {cities_result['updated']}"
        ))

        # Districts
        districts_result = import_locations.import_districts()
        self.stdout.write(self.style.SUCCESS(
            f"[DISTRICTS - TOTAL] Inserted: {districts_result['inserted']}, Updated: {districts_result['updated']}"
        ))
