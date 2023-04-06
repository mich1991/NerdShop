from django.urls import path, include
from .views import HomePageView, ContactPageView, AboutPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact-us', ContactPageView.as_view(), name='contact_us'),
    path('about-us', AboutPageView.as_view(), name='about_us')
]
