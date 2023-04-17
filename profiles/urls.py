from django.urls import path, include
from .views import ProfilePageView, OrdersPageView, OrderDetailsPageView

urlpatterns = [
    path('', ProfilePageView.as_view(), name='profiles'),
    path('orders', OrdersPageView.as_view(), name='user_orders'),
    path('orders/<int:pk>', OrderDetailsPageView.as_view(), name='user_order_details')

]
