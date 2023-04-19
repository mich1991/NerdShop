from django.shortcuts import get_object_or_404, reverse, redirect, \
	HttpResponse
from django.views.generic import TemplateView, View
from products.models import Product
from django.contrib import messages


# Create your views here.


class CartViewPage(TemplateView):
	template_name = 'cart/cart.html'


class CartAddView(View):
	def post(self, request, pk):
		"""Add a quantity of the specified product to the cart"""
		if request.POST.get('quantity'):
			quantity = int(request.POST.get('quantity'))
		else:
			quantity = 1
		product_id = str(pk)
		product = get_object_or_404(Product, pk=pk)
		redirect_url = request.POST.get('redirect_url')
		cart = request.session.get('cart', {})
		print(request.session.get('cart_items'))
		if product_id in list(cart.keys()):
			cart[product_id] += quantity
		else:
			cart[product_id] = quantity
		request.session['cart'] = cart
		messages.success(request,
		                 (f'Added {product.title} '
		                  f'quantity to {cart[product_id]}'))
		return redirect(redirect_url)


class CartUpdateView(View):
	def post(self, request, pk):
		product = get_object_or_404(Product, pk=pk)
		quantity = int(request.POST.get('quantity'))
		cart = request.session.get('cart', {})
		if quantity > 0:
			cart[pk] = quantity
			messages.success(request,
			                 (f'Updated {product.title} '
			                  f'quantity to {cart[pk]}'))
		else:
			cart.pop(pk)
			messages.success(request,
			                 (f'Removed {product.title} '
			                  f'from your cart'))

		request.session['cart'] = cart
		return redirect(reverse('view_cart'))


class CartDeleteView(View):
	def post(self, request, pk):
		try:
			product = get_object_or_404(Product, pk=pk)
			cart = request.session.get('cart', {})
			print(cart)
			cart.pop(str(pk))
			messages.success(request, f'Removed {product.title} from your cart')

			request.session['cart'] = cart
			return redirect(reverse('view_cart'))

		except Exception as e:
			messages.error(request, f'Error removing item: {e}')
			return HttpResponse(status=500)
