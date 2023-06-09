from django.shortcuts import render, redirect, reverse, HttpResponse, \
	get_object_or_404
from django.views.generic import View
from products.models import Product
from profiles.forms import ProfileForm
from .forms import OrderForm
from .models import OrderLineItem, Order
from django.contrib import messages
from cart.context import cart_contents
from profiles.models import Profile
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

import json
import stripe


class CheckoutViewPage(View):

	def get(self, request):
		stripe_public_key = settings.STRIPE_PUBLIC_KEY
		stripe_secret_key = settings.STRIPE_SECRET_KEY

		cart = request.session.get('cart', {})

		if not cart:
			messages.error(request,
			               "There's nothing in your cart at the moment")
			return redirect(reverse('product_list'))

		current_cart = cart_contents(request)
		total = current_cart['grand_total']
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

	def post(self, request):
		cart = request.session.get('cart', {})

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
			order.original_cart = json.dumps(cart)
			order.save()
			for item_id, item_data in cart.items():
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
						for size, quantity in item_data[
							'items_by_size'].items():
							order_line_item = OrderLineItem(
								order=order,
								product=product,
								quantity=quantity,
								product_size=size,
							)
							order_line_item.save()
				except Product.DoesNotExist:
					messages.error(request, (
						"One of the products in your cart wasn't "
						"found in our database. "
						"Please call us for assistance!")
					               )
					order.delete()
					return redirect(reverse('view_cart'))

			# Save the info to the user's profile if all is well
			request.session['save_info'] = 'save-info' in request.POST
			return redirect(reverse('checkout_success',
			                        args=[order.order_number]))


class CacheCheckoutDataView(View):
	def post(self, request):
		try:
			pid = request.POST.get('client_secret').split('_secret')[0]
			stripe.api_key = settings.STRIPE_SECRET_KEY
			stripe.PaymentIntent.modify(pid, metadata={
				'cart': json.dumps(request.session.get('cart', {})),
				'save_info': request.POST.get('save_info'),
				'username': request.user,
			})
			return HttpResponse(status=200)
		except Exception as e:
			messages.error(request, ('Sorry, your payment cannot be '
			                         'processed right now. Please try '
			                         'again later.'))
			return HttpResponse(content=e, status=400)


class CheckoutSuccessView(View):
	def get(self, request, order_number):
		"""
		   Handle successful checkouts
		   """
		save_info = request.session.get('save_info')
		order = get_object_or_404(Order, order_number=order_number)

		if request.user.is_authenticated:
			profile = Profile.objects.get(user=request.user)
			# Attach the user's profile to the order
			order.user_profile = profile
			order.save()

			# Save the user's info
			if save_info:
				profile_data = {
					'default_phone_number': order.phone_number,
					'default_postcode': order.postcode,
					'default_town_or_city': order.town_or_city,
					'default_street_address1': order.street_address1,
					'default_street_address2': order.street_address2,
					'default_county': order.county,
				}
				user_profile_form = ProfileForm(profile_data, instance=profile)
				if user_profile_form.is_valid():
					user_profile_form.save()

		messages.success(request, f'Order successfully processed! \
		       Your order number is {order_number}. A confirmation \
		       email will be sent to {order.email}.')

		cust_email = order.email
		subject = render_to_string(
			'checkout/confirmation_emails/confirmation_email_subject.txt',
			{'order': order})
		body = render_to_string(
			'checkout/confirmation_emails/confirmation_email_body.txt',
			{'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

		send_mail(
			subject,
			body,
			settings.DEFAULT_FROM_EMAIL,
			[cust_email]
		)

		if 'cart' in request.session:
			del request.session['cart']

		template = 'checkout/checkout_success.html'
		context = {
			'order': order,
		}

		return render(request, template, context)
