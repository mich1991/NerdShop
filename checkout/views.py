from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from products.models import Product
from .forms import OrderForm
from .models import OrderLineItem
from django.contrib import messages
from cart.context import cart_contents
from profiles.models import Profile
from django.conf import settings
# Create your views here.
import json
import stripe


class CheckoutViewPage(View):

	def get(self, request):
		stripe_public_key = settings.STRIPE_PUBLIC_KEY
		stripe_secret_key = settings.STRIPE_SECRET_KEY

		cart = request.session.get('cart', {})

		if not cart:
			messages.error(request,
			               "There's nothing in your bag at the moment")
			return redirect(reverse('product_list'))

		current_bag = cart_contents(request)
		total = current_bag['grand_total']
		stripe_total = round(total * 100)
		stripe.api_key = stripe_secret_key
		intent = stripe.PaymentIntent.create(
			amount=stripe_total,
			currency=settings.STRIPE_CURRENCY,
		)

		# Attempt to prefill the form with any info
		# the user maintains in their profile
		if request.user.is_authenticated:
			try:
				profile = Profile.objects.get(user=request.user)
				order_form = OrderForm(initial={
					'full_name': profile.profile_name,
					'email': profile.user.email,
					'phone_number': profile.profile_phone_nr,
					'postcode': profile.profile_postcode,
					'town_or_city': profile.profile_city,
					'street_address1': profile.profile_address_line1,
					'street_address2': profile.profile_address_line2,
					'county': profile.profile_county,
				})
			except Profile.DoesNotExist:
				order_form = OrderForm()
		else:
			order_form = OrderForm()

		if not stripe_public_key:
			messages.warning(request, ('Stripe public key is missing. '
			                           'Did you forget to set it in '
			                           'your environment?'))

		template = 'checkout/checkout.html'
		context = {
			'order_form': order_form,
			'stripe_public_key': stripe_public_key,
			'client_secret': intent.client_secret,
		}

		return render(request, 'checkout/checkout.html', context)

	# END OF COPY
	# return render(request, 'checkout/checkout.html')


def post(self, request):
	bag = request.session.get('bag', {})

	form_data = {
		'full_name': request.POST['full_name'],
		'email': request.POST['email'],
		'phone_number': request.POST['phone_number'],
		'postcode': request.POST['postcode'],
		'town_or_city': request.POST['town_or_city'],
		'street_address1': request.POST['street_address1'],
		'street_address2': request.POST['street_address2'],
		'county': request.POST['county'],
	}

	order_form = OrderForm(form_data)
	if order_form.is_valid():
		order = order_form.save(commit=False)
		pid = request.POST.get('client_secret').split('_secret')[0]
		order.stripe_pid = pid
		order.original_bag = json.dumps(bag)
		order.save()
		for item_id, item_data in bag.items():
			try:
				product = Product.objects.get(id=item_id)
				if isinstance(item_data, int):
					order_line_item = OrderLineItem(
						order=order,
						product=product,
						quantity=item_data,
					)
					order_line_item.save()
				else:
					for size, quantity in item_data['items_by_size'].items():
						order_line_item = OrderLineItem(
							order=order,
							product=product,
							quantity=quantity,
							product_size=size,
						)
						order_line_item.save()
			except Product.DoesNotExist:
				messages.error(request, (
					"One of the products in your bag wasn't "
					"found in our database. "
					"Please call us for assistance!")
				               )
				order.delete()
				return redirect(reverse('view_bag'))

		# Save the info to the user's profile if all is well
		request.session['save_info'] = 'save-info' in request.POST
		return redirect(reverse('checkout_success',
		                        args=[order.order_number]))


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
