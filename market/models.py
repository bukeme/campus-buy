from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from statistics import mean

User = get_user_model()

# Create your models here.


class ProductCategory(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	seller = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
	description = models.TextField()
	price = models.DecimalField(max_digits=6, decimal_places=2)
	location = models.CharField(max_length=500)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	@property
	def rating(self):
		try:
			result = mean([review.rating for review in self.reviews.all()])
		except:
			result = 0
		return round(result, 2)


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to='product_images/%Y-%m-%d/')
	thumbnail = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.product.name} Image'


class ProductReview(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(limit_value=0), MaxValueValidator(limit_value=5)])
	review = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.user}'s reviews on {self.product} product"

