from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, mixins, views, exceptions
from .serializers import (
	ProductCategorySerializer,
	ProductSerializer,
	ProductUpdateSerializer,
	ProductImageSerializer,
	ProductImageUpdateSerializer,
	ProductReviewSerializer
)
from .models import ProductCategory, Product, ProductImage, ProductReview
from .permissions import IsAdminOrReadOnly, IsProductOwnerOrReadOnly, IsImageOwnerOrReadOnly, IsProductReviewOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response



class ProductCategoryViewSet(viewsets.ModelViewSet):
	queryset = ProductCategory.objects.all()
	serializer_class = ProductCategorySerializer
	permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = [IsProductOwnerOrReadOnly]
	parser_classes = [MultiPartParser, FormParser]

	def get_queryset(self, *args, **kwargs):
		qs = super().get_queryset(*args, **kwargs)
		cat_query = request.GET.get('category', '')
		name_query = request.GET.get('name', '')
		result = qs.filter(
			category__name__icontains=cat_query,
			name__icontains=name_query
		)
		return result


	def perform_create(self, serializer):
		serializer.save(seller=self.request.user)
		return super().perform_create(serializer)

class ProductImageMixinView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
	queryset = ProductImage.objects.all()
	serializer_class = ProductImageSerializer
	permission_classes = [IsImageOwnerOrReadOnly]
	# parser_classes = [MultiPartParser, FormParser]
	def get(self, request, *args, **kwargs):
		if kwargs.get('pk'):
			return self.retrieve(request, *args, **kwargs)
		return self.list(request, *args, **kwargs)
	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

product_image_mixin_view = ProductImageMixinView.as_view()

class ProductImageCreateAPIView(views.APIView):
	def post(self, request, *args, **kwargs):
		data = request.data
		image_list = data.getlist('images')
		product = Product.objects.get(pk=int(request.data['product']))
		if request.user != product.seller:
			raise exceptions.PermissionDenied
		for image in image_list:
			ProductImage.objects.create(image=image, product=product)
		serializer = ProductImageSerializer(product.images.all(), many=True).data
		return Response(serializer)

product_image_create_apiview = ProductImageCreateAPIView.as_view()

class ProductImageUpdateAPIView(generics.UpdateAPIView):
	queryset = ProductImage.objects.all()
	serializer_class = ProductImageUpdateSerializer
	permission_classes = [IsImageOwnerOrReadOnly]

	def perform_update(self, serializer):
		thumbnail = serializer.validated_data['thumbnail']
		if thumbnail:
			product = self.get_object().product
			for image in product.images.all():
				image.thumbnail = False
				image.save()
		return super().perform_update(serializer)

product_image_update_api_view = ProductImageUpdateAPIView.as_view()


class ProductUpdateAPIView(generics.UpdateAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductUpdateSerializer
	permission_classes = [IsProductOwnerOrReadOnly]

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


class ProductReviewViewSet(viewsets.ModelViewSet):
	queryset = ProductReview.objects.all()
	serializer_class = ProductReviewSerializer
	permission_classes = [IsProductReviewOwnerOrReadOnly]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

