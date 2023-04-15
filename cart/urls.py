from django.urls import path
from .views import CartViewPage, CartAddView, CartDeleteView, CartUpdateView


urlpatterns = [
    path('', CartViewPage.as_view(), name='view_cart'),
    path('add/<int:pk>', CartAddView.as_view(), name='add_to_cart'),
    path('update/<int:pk>', CartUpdateView.as_view(), name='update_cart'),
    path('delete/<int:pk>', CartDeleteView.as_view(), name='delete_from_cart'),
]