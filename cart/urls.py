from django.urls import path
from .views import CartViewPage, CartAddView, CartDeleteView, CartUpdateView


urlpatterns = [
    path('', CartViewPage.as_view(), name='view_cart'),
    path('add/<item_id>/', CartAddView.as_view(), name='add_to_cart'),
    path('update/<item_id>/', CartUpdateView.as_view(), name='update_cart'),
    path('delete/<item_id>/', CartDeleteView.as_view(), name='delete_from_cart'),
]