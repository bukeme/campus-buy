from rest_framework import serializers
from .models import (
	ProductCategory,
	ProductImage,
	Product,
	ProductReview,
	ServiceCategory,
	ServiceImage,
	Service,
	ServiceReview
)
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


# SERVICES

class ServiceCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ServiceCategory
		fields = ['pk', 'name',]


class ServiceImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ServiceImage
		fields = ['pk', 'image', 'service', 'thumbnail']

class ServiceImageUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = ServiceImage
		fields = ['thumbnail']

class ServiceReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = ServiceReview
		fields = ['pk', 'service', 'user', 'rating', 'review', 'created', 'updated']
		read_only_fields = ['pk', 'user', 'created', 'updated']


class ServiceSerializer(serializers.ModelSerializer):
	images = ServiceImageSerializer(many=True, read_only=True)
	uploaded_images = serializers.ListField(
		child=serializers.ImageField(write_only=True, use_url=False, allow_empty_file=False),
		write_only=True,
		allow_null=True,
	)
	reviews = ServiceReviewSerializer(many=True, read_only=True)
	thumbnail = serializers.ImageField(write_only=True)
	category = ServiceCategorySerializer(many=False, read_only=True)
	sent_category = serializers.CharField(write_only=True)
	seller = UserSerializer(many=False, read_only=True)

	class Meta:
		model = Service
		fields = ['pk', 'seller', 'name', 'category', 'sent_category', 'description', 'location', 'images', 'uploaded_images', 'thumbnail', 'reviews', 'rating']

	def create(self, validated_data):
		uploaded_images = validated_data.pop('uploaded_images')
		thumbnail = validated_data.pop('thumbnail')
		category = validated_data.pop('sent_category')
		service_category = ServiceCategory.objects.filter(name__icontains=category)
		if service_category.exists():
			cat = service_category.first()
		else:
			cat = ServiceCategory.objects.create(name=category)
		service = Service.objects.create(**validated_data, category=cat)
		for image in uploaded_images:
			ServiceImage.objects.create(service=service, image=image)
		ServiceImage.objects.create(service=service, image=thumbnail, thumbnail=True)
		return service

class ServiceUpdateSerializer(serializers.ModelSerializer):
	category = ServiceCategorySerializer(many=False, read_only=True)
	sent_category = serializers.CharField(write_only=True)

	class Meta:
		model = Service
		fields = ['pk', 'name', 'category', 'sent_category', 'description', 'price', 'location',]

