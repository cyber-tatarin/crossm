from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import CreateCompanyView, CompanyPageView, DeleteCompanyView, UpdateCompanyView

app_name = 'companies'

urlpatterns = [
    path('create/', CreateCompanyView.as_view(), name='create-company'),
    path('<int:pk>/', CompanyPageView.as_view(), name='company-page'),
    path('delete/', DeleteCompanyView.as_view(), name='delete-company'),
    path('update/<int:pk>/', UpdateCompanyView.as_view(), name='update-company'),
]
