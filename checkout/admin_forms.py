from django import forms
from django_countries import countries
from .models import Order

class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force evaluation of country choices to prevent BlankChoiceIterator error
        self.fields['country'].choices = [('', 'Country *')] + list(countries)
