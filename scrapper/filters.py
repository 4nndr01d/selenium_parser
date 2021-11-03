import django_filters
from .models import *
from django import forms


class VacancyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label="Name")
    company = django_filters.ModelChoiceFilter(field_name="company", label="Company", queryset=Company.objects.all(), )
    class Meta:
        model = Vacancy
        fields = ['name', 'skills', 'company']

