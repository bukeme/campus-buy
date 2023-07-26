from rest_framework import serializers
from .models import ProductCategory, ProductImage, Product
from users.serializers import UserSerializer


class ProductCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductCategory
		fields = ['pk', 'name',]


class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = ['pk', 'image', 'product']


class ProductSerializer(serializers.ModelSerializer):
	images = ProductImageSerializer(many=True, read_only=True)
	uploaded_images = serializers.ListField(
		child=serializers.ImageField(write_only=True, use_url=False, allow_empty_file=False),
		write_only=True,
		allow_null=True,
	)
	category = ProductCategorySerializer(many=False, read_only=True)
	sent_category = serializers.CharField(write_only=True)
	seller = UserSerializer(many=False, read_only=True)

	class Meta:
		model = Product
		fields = ['pk', 'seller', 'name', 'category', 'sent_category', 'description', 'price', 'location', 'images', 'uploaded_images',]

	def create(self, validated_data):
		uploaded_images = validated_data.pop('uploaded_images')
		category = validated_data.pop('sent_category')
		product_category = ProductCategory.objects.filter(name__icontains=category)
		if product_category.exists():
			cat = product_category.first()
		else:
			cat = ProductCategory.objects.create(name=category)
		product = Product.objects.create(**validated_data, category=cat)
		for image in uploaded_images:
			ProductImage.objects.create(product=product, image=image)
		return product

class ProductUpdateSerializer(serializers.ModelSerializer):
	category = ProductCategorySerializer(many=False, read_only=True)
	sent_category = serializers.CharField(write_only=True)

	class Meta:
		model = Product
		fields = ['pk', 'name', 'category', 'sent_category', 'description', 'price', 'location',]