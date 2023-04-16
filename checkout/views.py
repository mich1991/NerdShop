from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class CheckoutViewPage(View):
	def get(self, request):
		return render(request, 'checkout/checkout.html')

	def post(self, request):
		return render(request, 'checkout/checkout.html')


class CacheCheckoutDataView(View):
	def get(self, request):
		return render(request, 'checkout/checkout.html')

	def post(self, request):
		return render(request, 'checkout/checkout.html')


class CheckoutSuccessView(View):
	def get(self, request):
		return render(request, 'checkout/checkout.html')

	def post(self, request):
		return render(request, 'checkout/checkout.html')
