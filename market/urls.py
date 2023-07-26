from rest_framework import routers
from django.urls import path
from .views import ProductCategoryViewSet, ProductViewSet, ProductImageViewSet, product_update



urlpatterns = [
	path('product/<int:pk>/', product_update),
]

router = routers.DefaultRouter()
router.register(r'product-category', ProductCategoryViewSet, basename='productcategory')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'product-image', ProductImageViewSet, basename='productimage')
urlpatterns += router.urls
