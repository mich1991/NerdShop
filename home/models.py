from django.db import models

# Create your models here.


class Contact(models.Model):
	email = models.EmailField()
	name = models.CharField(max_length=20)
	message = models.TextField()
	date = models.DateTimeField(auto_created=True, auto_now=True)

	def __str__(self):
		return f'{self.name} : {self.email}'


class NewsLetter(models.Model):
	email = models.EmailField()
	date = models.DateTimeField(auto_created=True, auto_now=True)

	def __str__(self):
		return self.email
