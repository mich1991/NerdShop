from django.urls import path
from . import views

urlpatterns = [
	path('admin-panel', views.AdminProductListView.as_view(),
	     name='admin_products_list'),
	path('admin-panel/add', views.AdminAddProductView.as_view(),
	     name='admin_add_product'),
	path('admin-panel/edit/<int:pk>', views.AdminEditProductView.as_view(),
	     name='admin_edit_product'),
	path('admin-panel/delete/<int:pk>', views.AdminDeleteProductView.as_view(),
	     name='admin_delete_product'),
	path('<slug:slug>', views.ProductDetailView.as_view(),
	     name='product_details'),
	path('', views.ProductListView.as_view(), name='product_list'),
]
