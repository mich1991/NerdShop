from django.contrib import admin
from .models import Contact, NewsLetter
# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_filter = ('name', 'email', 'date')
	list_display = ('name', 'email', 'message', 'date')
	search_fields = ['name', 'email', 'message']


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
	list_display = ('email', 'date')
	list_filter = ('email', 'date')
	search_fields = ['email', 'date']
