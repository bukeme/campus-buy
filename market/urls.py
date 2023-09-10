from rest_framework import routers
from django.urls import path
# from .views import ProductCategoryViewSet, ProductViewSet, product_update, product_image_mixin_view
from . import views



urlpatterns = [
	path('product/<int:pk>/', views.product_update),
	path('product-image/list/', views.product_image_mixin_view),
	path('product-image/<int:pk>/', views.product_image_mixin_view),
	path('product-image/<int:pk>/delete', views.product_image_mixin_view),
	path('product-image/create/', views.product_image_create_apiview),
	path('product-image/<int:pk>/update/', views.product_image_update_api_view),
]

router = routers.DefaultRouter()
router.register(r'product-category', views.ProductCategoryViewSet, basename='productcategory')
# router.register(r'product-image', views.ProductImageViewSet, basename='productimage')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'product-review', views.ProductReviewViewSet, basename='product_review')
urlpatterns += router.urls
