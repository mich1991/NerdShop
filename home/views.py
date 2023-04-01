from django.shortcuts import render
from django.views.generic import View
from products.models import Product
# Create your views here.


class HomePageView(View):
	def get(self, request):
		published_products = Product.objects.filter(status='1')
		ps5_latest_products = published_products.filter(platform__name='PS5').order_by('-created_on')[:4]
		xbox_latest_products = published_products.filter(platform__name='XBOX X/S').order_by('-created_on')[:4]
		switch_latest_products = published_products.filter(platform__name='SWITCH').order_by('-created_on')[:4]

		ctx = {
			'ps5': ps5_latest_products,
			'xbox': xbox_latest_products,
			'switch': switch_latest_products
		}
		return render(request, 'home/index.html', ctx)
