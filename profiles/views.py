from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.views.generic import View, ListView, DetailView

from checkout.models import Order
from .models import Profile
from .forms import ProfileForm


# Create your views here.


class ProfilePageView(View):
	def get(self, request):
		profile = get_object_or_404(Profile, user=request.user)
		form = ProfileForm(instance=profile)
		ctx = {
			'form': form
		}
		return render(request, 'profiles/profile.html', ctx)

	def post(self, request):
		profile = get_object_or_404(Profile, user=request.user)

		form = ProfileForm(request.POST, instance=profile)
		if form.is_valid():
			form.save()
			return redirect('profiles')
		ctx = {
			'form': form
		}
		return render(request, 'profiles/profile.html', ctx)


class OrdersPageView(View):
	def get(self, request):
		profile = get_object_or_404(Profile, user=request.user)
		orders = profile.orders.all().order_by('-date')
		ctx = {
			'orders': orders,
		}
		return render(request, 'profiles/orders.html', ctx)


class OrderDetailsPageView(DetailView):
	model = Order
	template_name = 'profiles/order_details.html'
