from django.views.generic import ListView
from .models import Company


class CompanyListView(ListView):
    model = Company
    template_name = 'pages/company_table.html'
    context_object_name = 'companies'
    paginate_by = 10