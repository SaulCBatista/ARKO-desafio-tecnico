from django.views.generic import ListView
from django.shortcuts import render, redirect
from .models import Company
from django.db.models import Count, Sum
import os
import tempfile
from django.contrib import messages
from django.views.decorators.http import require_POST
from companies.services import import_companies

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

@require_POST
def import_companies_view(request):
    uploaded_file = request.FILES.get('zip_file')
    if not uploaded_file:
        messages.error(request, "Nenhum arquivo enviado.")
        return redirect('dashboard')  # ajuste conforme o nome da sua view

    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp:
        for chunk in uploaded_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    try:
        import_companies(tmp_path)
        messages.success(request, "Importação realizada com sucesso.")
    except Exception as e:
        messages.error(request, f"Erro durante importação: {str(e)}")
    finally:
        os.remove(tmp_path)

    return redirect('dashboard')  # ajuste conforme necessário
