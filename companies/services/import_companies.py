import pandas as pd
import zipfile
from companies.models import Company
from django.db import transaction

COMPANY_SIZE_MAP = {
    '00': 'NÃO INFORMADO',
    '01': 'MICRO EMPRESA',
    '03': 'EMPRESA DE PEQUENO PORTE',
    '05': 'DEMAIS'
}

def clean_value(value):
    if pd.isna(value) or str(value).strip().lower() in ['nan', '', 'none']:
        return '-'
    return str(value).strip()

def map_company_size(code):
    code = clean_value(code)
    return COMPANY_SIZE_MAP.get(code.zfill(2), '-') if code != '-' else '-'

def import_companies(zip_path, chunksize=100_000):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        csv_file_name = zip_ref.namelist()[0]
        
        with zip_ref.open(csv_file_name) as csv_file:
            chunk_iterador = pd.read_csv(
                csv_file,
                sep=';',
                dtype=str,
                encoding='latin1',
                chunksize=chunksize,
                low_memory=False,
                header=None
            )

            for chunk in chunk_iterador:
                for _, row in chunk.iterrows():
                    basic_cnpj = clean_value(row[0])
                    corporate_name = clean_value(row[1])
                    legal_nature = clean_value(row[2])
                    responsible_qualification = clean_value(row[3])
                    raw_share_capital = clean_value(row[4])
                    company_size_code = clean_value(row[5])
                    federative_entity = clean_value(row[6])

                    try:
                        share_capital = float(raw_share_capital.replace(',', '.')) if raw_share_capital != '-' else 0.0
                    except ValueError:
                        share_capital = 0.0

                    company_size = map_company_size(company_size_code)

                    with transaction.atomic():
                        Company.objects.update_or_create(
                            basic_cnpj=basic_cnpj,
                            defaults={
                                'corporate_name': corporate_name,
                                'legal_nature': legal_nature,
                                'responsible_qualification': responsible_qualification,
                                'share_capital': share_capital,
                                'company_size': company_size,
                                'federative_entity': federative_entity
                            }
                        )
