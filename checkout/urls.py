from django.urls import path
from .views import CheckoutViewPage, CheckoutSuccessView, CacheCheckoutDataView
from .webhooks import webhook

urlpatterns = [
	path('', CheckoutViewPage.as_view(), name='checkout'),
	path('checkout_success/<order_number>', CheckoutSuccessView.as_view(), name='checkout_success'),
	path('cache_checkout_data/', CacheCheckoutDataView.as_view(), name='cache_checkout_data'),
	path('wh/', webhook, name="webhook")
]
