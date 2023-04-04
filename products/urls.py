from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('<slug:slug>', ProductDetailView.as_view(), name='product_details'),
    path('', ProductListView.as_view(), name='product_list'),
]
