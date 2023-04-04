from django.contrib import admin
from .models import Contact
# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_filter = ('name', 'email', 'date')
	list_display = ('name', 'email', 'message', 'date')
	search_fields = ['name', 'email', 'message']

