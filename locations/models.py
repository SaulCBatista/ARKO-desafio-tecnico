from django.db import models

class State(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, null=False, blank=False)
    acronym = models.CharField(max_length=2, null=False, blank=False)
    region = models.CharField(max_length=32, null=False, blank=False)

class City(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, null=False, blank=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

class District(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, null=False, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts')


