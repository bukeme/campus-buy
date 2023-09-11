from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, mixins, views, exceptions
from .serializers import (
	ProductCategorySerializer,
	ProductSerializer,
	ProductUpdateSerializer,
	ProductImageSerializer,
	ProductImageUpdateSerializer,
	ProductReviewSerializer,
	ServiceCategorySerializer,
	ServiceSerializer,
	ServiceUpdateSerializer,
	ServiceImageSerializer,
	ServiceImageUpdateSerializer,
	ServiceReviewSerializer
)
from .models import (
	ProductCategory,
	Product,
	ProductImage,
	ProductReview,
	ServiceCategory,
	Service,
	ServiceImage,
	ServiceReview
)
from .permissions import IsAdminOrReadOnly, IsProductOwnerOrReadOnly, IsImageOwnerOrReadOnly, IsProductReviewOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response



class ProductCategoryViewSet(viewsets.ModelViewSet):
	queryset = ProductCategory.objects.all()
	serializer_class = ProductCategorySerializer
	permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
	serializer_class = ProductSerializer
	permission_classes = [IsProductOwnerOrReadOnly]
	parser_classes = [MultiPartParser, FormParser]

	def get_queryset(self, *args, **kwargs):
		category = self.request.GET.get('category', '')
		name = self.request.GET.get('name', '')
		result = Product.objects.filter(
			category__name__icontains=category,
			name__icontains=name
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


class UserProductListAPIView(generics.ListAPIView):
	serializer_class = ProductSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self, *args, **kwargs):
		return Product.objects.filter(seller=self.request.user)

user_product_list_api_view = UserProductListAPIView.as_view()


# SERVICE

class ServiceCategoryViewSet(viewsets.ModelViewSet):
	queryset = ServiceCategory.objects.all()
	serializer_class = ServiceCategorySerializer
	permission_classes = [IsAdminOrReadOnly]


class ServiceViewSet(viewsets.ModelViewSet):
	serializer_class = ServiceSerializer
	permission_classes = [IsProductOwnerOrReadOnly]
	parser_classes = [MultiPartParser, FormParser]

	def get_queryset(self, *args, **kwargs):
		category = self.request.GET.get('category', '')
		name = self.request.GET.get('name', '')
		result = Service.objects.filter(
			category__name__icontains=category,
			name__icontains=name
		)
		return result


	def perform_create(self, serializer):
		serializer.save(seller=self.request.user)
		return super().perform_create(serializer)

class ServiceImageMixinView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
	queryset = ServiceImage.objects.all()
	serializer_class = ServiceImageSerializer
	# permission_classes = [IsImageOwnerOrReadOnly]
	def get(self, request, *args, **kwargs):
		if kwargs.get('pk'):
			return self.retrieve(request, *args, **kwargs)
		return self.list(request, *args, **kwargs)
	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

service_image_mixin_view = ServiceImageMixinView.as_view()

class ServiceImageCreateAPIView(views.APIView):
	def post(self, request, *args, **kwargs):
		data = request.data
		image_list = data.getlist('images')
		service = Service.objects.get(pk=int(request.data['service']))
		if request.user != service.seller:
			raise exceptions.PermissionDenied
		for image in image_list:
			ServiceImage.objects.create(image=image, service=service)
		serializer = ServiceImageSerializer(service.images.all(), many=True).data
		return Response(serializer)

service_image_create_apiview = ServiceImageCreateAPIView.as_view()

class ServiceImageUpdateAPIView(generics.UpdateAPIView):
	queryset = ServiceImage.objects.all()
	serializer_class = ServiceImageUpdateSerializer
	# permission_classes = [IsImageOwnerOrReadOnly]

	def perform_update(self, serializer):
		thumbnail = serializer.validated_data['thumbnail']
		if thumbnail:
			service = self.get_object().service
			for image in service.images.all():
				image.thumbnail = False
				image.save()
		return super().perform_update(serializer)

service_image_update_api_view = ServiceImageUpdateAPIView.as_view()


class ServiceUpdateAPIView(generics.UpdateAPIView):
	queryset = Service.objects.all()
	serializer_class = ServiceUpdateSerializer
	permission_classes = [IsProductOwnerOrReadOnly]

	def perform_update(self, serializer):
		category = serializer.validated_data['sent_category']
		service_category = ServiceCategory.objects.filter(name=category)
		if service_category.exists():
			cat = service_category.first()
		else:
			cat = serviceCategory.objects.create(name=category)
		serializer.save(category=cat)
		return super().perform_update(serializer)

service_update = ServiceUpdateAPIView.as_view()


class ServiceReviewViewSet(viewsets.ModelViewSet):
	queryset = ServiceReview.objects.all()
	serializer_class = ServiceReviewSerializer
	permission_classes = [IsProductReviewOwnerOrReadOnly]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class UserServiceListAPIView(generics.ListAPIView):
	serializer_class = ServiceSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self, *args, **kwargs):
		return Service.objects.filter(seller=self.request.user)

user_service_list_api_view = UserServiceListAPIView.as_view()

