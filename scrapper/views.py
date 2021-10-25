from django.shortcuts import redirect
from django.views.generic.edit import FormView
from .forms import FindForm
from django.http import HttpResponse


class MAIN(FormView):
    template_name = 'main.html'
    form_class = FindForm
    def form_valid(self, form):
        form.scrapp_work()
        msg = "Thanks for the review!"
        return redirect('main')

