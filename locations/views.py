from django.views.generic import ListView
from django.shortcuts import render
from .models import State, City, District

def dashboard_view(request):
    return render(request, 'pages/dashboard.html')

class StateListView(ListView):
    model = State
    template_name = 'pages/state_table.html'
    context_object_name = 'states'
    paginate_by = 10

class CityListView(ListView):
    model = City
    template_name = 'pages/city_table.html'
    context_object_name = 'cities'
    paginate_by = 10
    
class DistrictListView(ListView):
    model = District
    template_name = 'pages/district_table.html'
    context_object_name = 'district'
    paginate_by = 10