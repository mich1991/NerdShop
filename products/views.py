from django.shortcuts import render, get_object_or_404, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View, DeleteView
from .models import Product, Category, Platform
from django.contrib.auth.decorators import user_passes_test
from django.utils.text import slugify
from .forms import ProductForm
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


@method_decorator(user_passes_test(lambda u: u.is_staff, login_url='home',), name='dispatch')
class AdminProductListView(ListView):
	"""GET List of products that's belongs to an admin"""
	model = Product
	template_name = 'products/admin/admin_product_list.html'
	paginate_by = 10

	def get_queryset(self, **kwargs):
		url_query = self.request.GET
		base_query = super().get_queryset().order_by('-created_on')
		if url_query.get('title'):
			base_query = base_query.filter(title__icontains=url_query.get('title'))
		if url_query.get('category'):
			base_query = base_query.filter(category__name=url_query.get('category'))
		if url_query.get('category'):
			base_query = base_query.filter(platform__name=url_query.get('platform'))
		return base_query

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		context['platforms'] = Platform.objects.all()
		context['form'] = {
			'title': self.request.GET.get('title') if self.request.GET.get('title') else '',
			'category': self.request.GET.get('category') if self.request.GET.get('category') else '',
			'platform': self.request.GET.get('platform') if self.request.GET.get('platform') else '',
		}
		return context


@method_decorator(user_passes_test(lambda u: u.is_staff, login_url='home',), name='dispatch')
class AdminAddProductView(View):
	def get(self, request):
		ctx = {
			'form': ProductForm()
		}
		return render(request, 'products/admin/admin_add_product.html', ctx)

	def post(self, request):
		form = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			product = form.save(commit=False)
			product.slug = slugify(product.title)
			product.author = request.user
			product.save()
			form = ProductForm()
			ctx = {
				'form': form,
				'success': True
			}
			return render(request, 'products/admin/admin_add_product.html', ctx)
		ctx = {'form': form}
		return render(request, 'products/admin/admin_add_product.html', ctx)


@method_decorator(user_passes_test(lambda u: u.is_staff, login_url='home',), name='dispatch')
class AdminEditProductView(View):
	def get(self, request, pk):
		product = Product.objects.get(pk=pk)
		ctx = {
			'form': ProductForm(instance=product),
			'edit': True,
		}
		return render(request, 'products/admin/admin_add_product.html', ctx)

	def post(self, request, pk):
		product_instance = Product.objects.get(pk=pk)
		form = ProductForm(request.POST, request.FILES, instance=product_instance)
		if form.is_valid():
			product = form.save(commit=False)
			product.slug = slugify(product.title)
			product.admin = request.user
			product.save()
			ctx = {
				'form': form,
				'success': True,
				'edit': True,
			}
			return render(request, 'products/admin/admin_add_product.html', ctx)
		ctx = {
			'form': form,
			'edit': True,
		}
		return render(request, 'products/admin/admin_add_product.html', ctx)


@method_decorator(user_passes_test(lambda u: u.is_staff, login_url='/',), name='dispatch')
class AdminDeleteProductView(DeleteView):
	template_name = 'products/admin/admin_delete_product.html'

	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(Product, pk=pk)

	def get_success_url(self):
		return reverse('admin_products_list')
