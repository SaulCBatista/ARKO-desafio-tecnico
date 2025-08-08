# locations/services/ibge_importer.py
import requests
from requests.exceptions import RequestException
from locations.models import State, City, District


def import_states():
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    try:
        data = requests.get(url, timeout=10).json()
    except RequestException as e: 
        return {'error': f'[EXCEPTION - STATES] FAILED to request data: {e}'}

    existing_states = State.objects.in_bulk()

    inserted, updated, skipped = 0, 0, 0

    for state in data:
        state_id = state['id']
        defaults = {
            'name': state['nome'],
            'acronym': state['sigla'],
            'region': state['regiao']['nome'],
        }

        if state_id in existing_states:
            obj = existing_states[state_id]
            if (obj.name != defaults['name'] or
                obj.acronym != defaults['acronym'] or
                obj.region != defaults['region']):
                for field, value in defaults.items():
                    setattr(obj, field, value)
                obj.save(update_fields=list(defaults.keys()))
                updated += 1
            else:
                skipped += 1
        else:
            State.objects.create(id=state_id, **defaults)
            inserted += 1

    return {'inserted': inserted, 'updated': updated, 'skipped': skipped}


def import_cities():
    states = State.objects.all()
    existing_cities = City.objects.in_bulk()

    total_inserted, total_updated, total_skipped = 0, 0, 0

    for state in states:
        url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{state.id}/municipios'
        try:
            data = requests.get(url, timeout=10).json()
        except RequestException as e:
            print(f'[EXCEPTION - CITIES] FAILED to request data State {state.name}: {e}')
            continue

        inserted, updated, skipped = 0, 0, 0

        for city in data:
            city_id = city['id']
            defaults = {
                'name': city['nome'],
                'state': state
            }

            if city_id in existing_cities:
                obj = existing_cities[city_id]
                if obj.name != defaults['name'] or obj.state_id != state.id:
                    obj.name = defaults['name']
                    obj.state = state
                    obj.save(update_fields=['name', 'state'])
                    updated += 1
                else:
                    skipped += 1
            else:
                City.objects.create(id=city_id, **defaults)
                inserted += 1

        print(f'[CITIES - {state.acronym}] Inserted: {inserted}, Updated: {updated}, Skipped: {skipped}')
        total_inserted += inserted
        total_updated += updated
        total_skipped += skipped

    return {'inserted': total_inserted, 'updated': total_updated, 'skipped': total_skipped}


def import_districts():
    cities = City.objects.all()
    existing_districts = District.objects.in_bulk()

    total_inserted, total_updated, total_skipped = 0, 0, 0

    for city in cities:
        url = f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{city.id}/distritos'
        try:
            data = requests.get(url, timeout=10).json()
        except RequestException as e:
            print(f'[EXCEPTION - DISTRICTS] FAILED to request data City {city.name}: {e}')
            continue

        inserted, updated, skipped = 0, 0, 0

        for district in data:
            district_id = district['id']
            defaults = {
                'name': district['nome'],
                'city': city
            }

            if district_id in existing_districts:
                obj = existing_districts[district_id]
                if obj.name != defaults['name'] or obj.city_id != city.id:
                    obj.name = defaults['name']
                    obj.city = city
                    obj.save(update_fields=['name', 'city'])
                    updated += 1
                else:
                    skipped += 1
            else:
                District.objects.create(id=district_id, **defaults)
                inserted += 1

        print(f'[DISTRICTS - {city.name}] Inserted: {inserted}, Updated: {updated}, Skipped: {skipped}')
        total_inserted += inserted
        total_updated += updated
        total_skipped += skipped

    return {'inserted': total_inserted, 'updated': total_updated, 'skipped': total_skipped}
