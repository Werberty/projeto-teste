from django.urls import include, path
from . import views

app_name = 'testes'

urlpatterns = [
    path('page_date/', views.page_dates),
    path('calculator_date/', views.calculator_dates, name='calculator_date'),
]