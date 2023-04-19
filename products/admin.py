from django.contrib import admin
from .models import Product, Category, Platform
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.

@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	summernote_fields = ('long_description',)
	list_display = (
	'title', 'category', 'platform', 'price', 'on_sale', 'sale_price',
	'created_on', 'updated_on', 'stock', 'status')
	list_filter = (
	'category', 'author', 'created_on', 'updated_on', 'stock', 'status')
	ordering = ('created_on',)
	search_fields = ['sku', 'title', 'long_description', 'short_description']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)
	list_filter = ('name',)


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
	list_display = ('name',)
	list_filter = ('name',)
