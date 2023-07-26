from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import ProductCategorySerializer, ProductSerializer, ProductUpdateSerializer, ProductImageSerializer
from .models import ProductCategory, Product, ProductImage
from rest_framework.parsers import MultiPartParser, FormParser



class ProductCategoryViewSet(viewsets.ModelViewSet):
	queryset = ProductCategory.objects.all()
	serializer_class = ProductCategorySerializer
	permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = [IsAuthenticated]
	parser_classes = [MultiPartParser, FormParser]

	def perform_create(self, serializer):
		serializer.save(seller=self.request.user)
		return super().perform_create(serializer)

class ProductImageViewSet(viewsets.ModelViewSet):
	queryset = ProductImage.objects.all()
	serializer_class = ProductImageSerializer
	permission_classes = [IsAuthenticated]
	parser_classes = [MultiPartParser, FormParser]


class ProductUpdateAPIView(generics.UpdateAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductUpdateSerializer
	permission_classes = [IsAuthenticated]

	def perform_update(self, serializer):
		category = serializer.validated_data['sent_category']
		product_category = ProductCategory.objects.filter(name=category)
		if product_category.exists():
			cat = product_category.first()
		else:
			cat = ProductCategory.objects.create(name=category)
		serializer.save(category=cat)
		return super().perform_update(serializer)

product_update = ProductUpdateAPIView.as_view()
