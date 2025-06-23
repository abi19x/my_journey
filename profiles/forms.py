from django import forms
from .models import UserProfile
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class UserProfileForm(forms.ModelForm):
    default_country = forms.TypedChoiceField(
        choices=[('', 'Country *')] + list(CountryField().choices),
        widget=CountrySelectWidget(attrs={
            'class': 'border-black rounded-0 profile-form-input'
        }),
        required=False
    )

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders.get(field, field)} *'
                else:
                    placeholder = placeholders.get(field, field)
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False
        else:
            # Country field already styled above, just hide label
            self.fields[field].label = False
