from django import forms
from .tasks import scrapping_work

class FindForm(forms.Form):
    city = forms.CharField(
        label='City', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'City', 'id': 'form-city'}))
    language = forms.CharField(
        max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Language', 'id': 'form-language'}))

    def scrapp_work(self):
        scrapping_work.delay('https://www.work.ua/jobs-kyiv-python/',self.cleaned_data['city'], self.cleaned_data['language'])

