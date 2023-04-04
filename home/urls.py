from django.urls import path, include
from .views import HomePageView, ContactPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact-us', ContactPageView.as_view(), name='contact_us' )
]
