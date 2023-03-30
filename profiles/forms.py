from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'profile_name': 'Full Name',
            'profile_phone_nr': 'Phone Number',
            'profile_postcode': 'Postal Code',
            'profile_city': 'City',
            'profile_address_line1': 'Street Address 1',
            'profile_address_line2': 'Street Address 2',
            'profile_county': 'County',
        }
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False