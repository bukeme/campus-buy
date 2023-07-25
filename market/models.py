from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Product(models.Model):
	seller = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	description = models.TextField()
	price = models.DecimalField(max_digits=6, decimal_places=2)
	location = models.CharField(max_length=500)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name


class Image(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='product_images/%Y-%m-%d/')
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.product.name} Image'

