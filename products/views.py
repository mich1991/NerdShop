from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from .models import Product, Category, Platform
# Create your views here.


class ProductListView(ListView):
	model = Product
	template_name = 'products/product_list.html'
	paginate_by = 12

	def get_queryset(self, **kwargs):
		url_query = self.request.GET
		base_query = super().get_queryset().filter(status='1', stock='1').order_by('-created_on')
		if url_query.get('title'):
			base_query = base_query.filter(title__icontains=url_query.get('title'))
		if url_query.get('category'):
			base_query = base_query.filter(category__name=url_query.get('category'))
		if url_query.get('platform'):
			base_query = base_query.filter(platform__name=url_query.get('platform'))
		return base_query

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		context['platforms'] = Platform.objects.all()
		context['form'] = {
			'title': self.request.GET.get('title') if self.request.GET.get('title') else '',
			'category': self.request.GET.get('category') if self.request.GET.get('category') else '',
			'platform': self.request.GET.get('platform') if self.request.GET.get('platform') else ''
		}
		return context


class ProductDetailView(View):

	def get(self, request, slug):
		queryset = Product.objects.filter(status=1)
		product = get_object_or_404(queryset, slug=slug)

		ctx = {
			'product': product,
		}
		return render(request, 'products/product_details.html', ctx)
