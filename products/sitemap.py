from django.contrib.sitemaps import Sitemap
from .models import Product


class ProductSitemap(Sitemap):
	# define how often your website will change, the priority, and the protocol used to access your site
	changefreq = 'weekly'  # can be weekly daily always monthly yearly or never
	priority = 1.0  # on a scale of 0.0 to 1.0
	protocol = 'http'  # use https when you deploy your website and are using a secure connection
	# TODO: check why project on heroku is deployed as HTTP

	def items(self):
		# only published products apply
		return Product.objects.all().filter(status='1')

	# will return the last time an article was updated
	def lastmod(self, obj):
		return obj.created_on

	# returns the URL of the product object
	def location(self, obj):
		return f'/shop/{obj.slug}'