from django.urls import path, include
from .views import HomePageView, ContactPageView, AboutPageView, \
	PoliciesPageView, NewsLetterView

urlpatterns = [
	path('', HomePageView.as_view(), name='home'),
	path('contact-us', ContactPageView.as_view(), name='contact_us'),
	path('about-us', AboutPageView.as_view(), name='about_us'),
	path('policies', PoliciesPageView.as_view(), name='policies'),
	path('newsletter', NewsLetterView.as_view(), name='news_letter')
]
