from django.db import models

class Company(models.Model):
    basic_cnpj = models.CharField(max_length=8, unique=True)
    corporate_name = models.CharField(max_length=200)
    legal_nature = models.CharField(max_length=3)
    responsible_qualification = models.CharField(max_length=2)
    share_capital = models.DecimalField(max_digits=20, decimal_places=2)
    company_size = models.CharField(max_length=1)             
    federative_entity = models.CharField(max_length=1)        

