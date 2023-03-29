from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class ProfilePageView(View):
	def get(self, request):
		return render(request, 'profiles/profile.html')


class OrdersPageView(View):
	def get(self, request):
		return render(request, 'profiles/orders.html')
