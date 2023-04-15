from .models import Product
from django import forms
from django_summernote.widgets import SummernoteWidget


class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		exclude = ('author', 'slug',)
		widgets = {
			'long_description': SummernoteWidget(),
		}
