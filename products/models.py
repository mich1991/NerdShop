from django.db import models

# Create your models here.

STATUS = ((0, 'Draft'), (1, 'Published'))
STOCK = ((0, 'Out of Stock'), (1, 'In Stock'))


class Category(models.Model):
	class Meta:
		verbose_name_plural = 'Categories'

	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name

