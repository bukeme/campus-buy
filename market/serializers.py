from rest_framework import serializers
from .models import ProductCategory, ProductImage, Product, ProductReview
from users.serializers import UserSerializer


class ProductCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductCategory
		fields = ['pk', 'name',]


class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = ['pk', 'image', 'product', 'thumbnail']

class ProductImageUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = ['thumbnail']

class ProductReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductReview
		fields = ['pk', 'product', 'user', 'rating', 'review', 'created', 'updated']
		read_only_fields = ['pk', 'user', 'created', 'updated']


class ProductSerializer(serializers.ModelSerializer):
	images = ProductImageSerializer(many=True, read_only=True)
	uploaded_images = serializers.ListField(
		child=serializers.ImageField(write_only=True, use_url=False, allow_empty_file=False),
		write_only=True,
		allow_null=True,
	)
	reviews = ProductReviewSerializer(many=True, read_only=True)
	thumbnail = serializers.ImageField(write_only=True)
	category = ProductCategorySerializer(many=False, read_only=True)
	sent_category = serializers.CharField(write_only=True)
	seller = UserSerializer(many=False, read_only=True)

	class Meta:
		model = Product
		fields = ['pk', 'seller', 'name', 'category', 'sent_category', 'description', 'price', 'location', 'images', 'uploaded_images', 'thumbnail', 'reviews', 'rating']

	def create(self, validated_data):
		uploaded_images = validated_data.pop('uploaded_images')
		thumbnail = validated_data.pop('thumbnail')
		category = validated_data.pop('sent_category')
		product_category = ProductCategory.objects.filter(name__icontains=category)
		if product_category.exists():
			cat = product_category.first()
		else:
			cat = ProductCategory.objects.create(name=category)
		product = Product.objects.create(**validated_data, category=cat)
		for image in uploaded_images:
			ProductImage.objects.create(product=product, image=image)
		ProductImage.objects.create(product=product, image=thumbnail, thumbnail=True)
		return product

class ProductUpdateSerializer(serializers.ModelSerializer):
	category = ProductCategorySerializer(many=False, read_only=True)
	sent_category = serializers.CharField(write_only=True)

	class Meta:
		model = Product
		fields = ['pk', 'name', 'category', 'sent_category', 'description', 'price', 'location',]

