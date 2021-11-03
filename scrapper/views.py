from django.shortcuts import redirect, render, get_object_or_404
from .forms import FindForm
from .models import Vacancy
from django.core.paginator import Paginator
from .filters import VacancyFilter
from .tasks import area_scrapping, scrapping_hh


def vacancies_list(request):
    form = FindForm()
    filter = VacancyFilter(request.GET, queryset=Vacancy.objects.all())
    vacancies = filter.qs

    paginator = Paginator(vacancies, 5)
    page_number = request.GET.get('page')
    vacancies = paginator.get_page(page_number)
    return render(request, 'home.html', {'vacancies': vacancies, 'form': form, 'filter': filter})


def vacancy_detail(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, vacancy_id=vacancy_id)
    return render(request, 'vacancy_detail.html', {'vacancy': vacancy})

def scrapper(request):
    # scrapping_hh.delay('python')
    return render(request, 'scrapper.html')

def parse_area(request):
    # area_scrapping.delay()
    scrapping_hh.delay('python')
    return redirect('scrapper')