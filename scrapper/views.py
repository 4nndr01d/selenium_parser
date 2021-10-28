from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from .forms import FindForm
from django.http import HttpResponse
from .models import Vacancy
from django.core.paginator import Paginator


def vacancies_list(request):
    form = FindForm()
    vacancies = Vacancy.objects.all()
    paginator = Paginator(vacancies, 5)
    page_number = request.GET.get('page')
    vacancies = paginator.get_page(page_number)
    return render(request, 'home.html', {'vacancies': vacancies, 'form': form})
# template_name = 'home.html'
# form_class = FindForm
# def form_valid(self, form):
#     form.scrapp_work()
#     msg = "Thanks for the review!"
#     return redirect('main')
