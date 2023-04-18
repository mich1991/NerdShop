from django.shortcuts import render, redirect, reverse
from django.views.generic import View, TemplateView
from products.models import Product
from .forms import ContactForm, NewsLetterForm
from django.contrib import messages
# Create your views here.


class HomePageView(View):
	def get(self, request):
		published_products = Product.objects.filter(status='1').filter(stock=1)
		ps5_latest_products = published_products.filter(platform__name='PS5').order_by('-created_on')[:4]
		xbox_latest_products = published_products.filter(platform__name='XBOX X/S').order_by('-created_on')[:4]
		switch_latest_products = published_products.filter(platform__name='SWITCH').order_by('-created_on')[:4]
		print(request)
		ctx = {
			'ps5': ps5_latest_products,
			'xbox': xbox_latest_products,
			'switch': switch_latest_products
		}
		return render(request, 'home/index.html', ctx)


class ContactPageView(View):
	def get(self, request):
		form = ContactForm()
		ctx = {'form': form}
		return render(request, 'home/contact.html', ctx)

	def post(self, request):
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			form = ContactForm()
			ctx = {
				'form': form,
				}
			return render(request, 'home/contact.html', ctx)
		ctx = {'form': form}
		return render(request, 'home/contact.html', ctx)


class AboutPageView(TemplateView):
	template_name = 'home/about.html'


class PoliciesPageView(TemplateView):
	template_name = 'home/policies.html'


class NewsLetterView(View):
	def get(self):
		return reverse('home')

	def post(self, request):
		form = NewsLetterForm(request.POST)
		if form.is_valid():
			form.save()
			form = NewsLetterForm()
			messages.success(request, 'Successfully signed up to a newsletter. Welcome aboard!')
			return redirect('home')
		ctx = {'form': form}
		messages.warning(request, "Are you sure that was corrected email address? Try again")
		return redirect('home', ctx)
