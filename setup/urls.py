from django.contrib import admin
from django.urls import path

from locations.views import StateListView, dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_view, name='dashboard'),
    path('states-table/', StateListView.as_view(), name='state_list')
]
