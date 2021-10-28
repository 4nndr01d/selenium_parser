from django.utils import timezone

from django.db import models
from django.conf import settings

class Skill(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Vacancy(models.Model):
    name = models.CharField(max_length=200)
    vacancy_id = models.IntegerField(unique=True)
    description = models.TextField()
    salary = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    skills = models.ManyToManyField(Skill)
    company = models.ForeignKey('scrapper.Company', on_delete=models.CASCADE, related_name='vacancies', blank=True)
    def __str__(self):
        return self.name


