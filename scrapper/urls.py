
from django.urls import path
from . import views

urlpatterns = [
    path('', views.vacancies_list, name='vacancies_list'),
    path('vacancy/<int:vacancy_id>', views.vacancy_detail, name='vacancy_detail'),
    path('scrapper', views.scrapper, name='scrapper'),
    path('parse_area', views.parse_area, name='parse_area'),
]