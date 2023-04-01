from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = ((0, 'Draft'), (1, 'Published'))
STOCK = ((0, 'Out of Stock'), (1, 'In Stock'))


class Platform(models.Model):
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name


class Category(models.Model):
	class Meta:
		verbose_name_plural = 'Categories'

	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name


class Product(models.Model):
	title = models.CharField(max_length=254, unique=True)
	short_description = models.CharField(max_length=200)
	long_description = models.TextField()
	sku = models.CharField(max_length=254, null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	image_url = models.URLField(max_length=1024, null=True, blank=True)
	slug = models.SlugField(unique=True)
	status = models.IntegerField(choices=STATUS, default=0)
	stock = models.IntegerField(choices=STOCK, default=0)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='category', null=True)
	platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, related_name='platform', null=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	on_sale = models.BooleanField(default=False, null=True, blank=True)
	sale_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	has_review = models.BooleanField(default=False, null=True, blank=True)
	review_url = models.URLField(max_length=1024, null=True, blank=True)

	def __str__(self):
		return self.title
