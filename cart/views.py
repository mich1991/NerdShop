from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView, TemplateView, DeleteView, View
from products.models import Product
from django.contrib import messages
# Create your views here.


class CartViewPage(ListView):
    template_name = 'cart/cart.html'


class CartAddView(View):
    def get(self, request):
        return render(request, 'cart/cart.html')

    def post(self, request):
        return render(request, 'cart/cart.html')


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
