from django.views.generic import ListView
from django.shortcuts import render
from .models import Company
from django.db.models import Count, Sum


class CompanyListView(ListView):
    model = Company
    template_name = 'pages/company_table.html'
    context_object_name = 'companies'
    paginate_by = 10

def dashboard_view(request):
    company_size_count = Company.objects.values('company_size').annotate(count=Count('id'))

    company_size_capital = Company.objects.values('company_size').annotate(total_capital=Sum('share_capital'))

    top_companies = Company.objects.order_by('-share_capital')[:5]

    context = {
        'company_size_count': list(company_size_count),
        'company_size_capital': [
            {'company_size': item['company_size'], 'total_capital': float(item['total_capital'] or 0)}
            for item in company_size_capital
        ],
        'top_companies': top_companies,
    }

    return render(request, 'pages/dashboard.html', context)