from django.views.generic import ListView
from django.shortcuts import render
from .models import State

def dashboard_view(request):
    return render(request, 'pages/dashboard.html')

class StateListView(ListView):
    model = State
    template_name = 'pages/state_table.html'
    context_object_name = 'states'
    paginate_by = 10
