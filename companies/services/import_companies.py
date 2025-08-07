import pandas as pd
import zipfile
from companies.models import Company
from django.db import transaction

def import_companies(zip_path, chunksize=100_000):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        csv_file_name = zip_ref.namelist()[0]
        
        with zip_ref.open(csv_file_name) as csv_file:
            chunk_iterador = pd.read_csv(
                csv_file,
                sep=';',
                dtype={
                    'BASIC_CNPJ': str,
                    'CORPORATE_NAME': str,
                    'LEGAL_NATURE': str,
                    'RESPONSIBLE_QUALIFICATION': str,
                    'SHARE_CAPITAL': str,
                    'COMPANY_SIZE': str,
                    'FEDERATIVE_ENTITY': str,
                },
                encoding='latin1',
                chunksize=chunksize,
                low_memory=False,
                header=None
            )

            for chunk in chunk_iterador:
                for _, row in chunk.iterrows():
                    try:
                        capital = float(str(row[4]).replace(',', '.'))
                    except ValueError:
                        capital = 0.0

                    with transaction.atomic():
                        Company.objects.update_or_create(
                            basic_cnpj=str(row[0]).strip(),
                            defaults={
                                'corporate_name': str(row[1]).strip(),
                                'legal_nature': str(row[2]).strip(),
                                'responsible_qualification': str(row[3]).strip(),
                                'share_capital': capital,
                                'company_size': str(row[5]).strip(),
                                'federative_entity': str(row[6]).strip()
                            }
                        )
