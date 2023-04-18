from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import TemplateView, DeleteView, View
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
        redirect_url = request.POST.get('redirect_url')
        cart = request.session.get('cart', {})
        print(request.session.get('cart_items'))
        if product_id in list(cart.keys()):
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity
        request.session['cart'] = cart
        return redirect(redirect_url)


class CartUpdateView(View):
    def get(self, request):
        return render(request, 'cart/cart.html')

    def post(self, request):
        return render(request, 'cart/cart.html')


class CartDeleteView(DeleteView):
    template_name = 'products/admin/admin_delete_product.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Product, pk=pk)

    def get_success_url(self):
        return reverse('admin_products_list')
