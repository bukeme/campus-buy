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
	path('user-products/', views.user_product_list_api_view),
	#SERVICES
	path('service/<int:pk>/', views.service_update),
	path('service-image/list/', views.service_image_mixin_view),
	path('service-image/<int:pk>/', views.service_image_mixin_view),
	path('service-image/<int:pk>/delete/', views.service_image_mixin_view),
	path('service-image/create/', views.service_image_create_apiview),
	path('service-image/<int:pk>/update/', views.service_image_update_api_view),
	path('user-services/', views.user_service_list_api_view),
]

router = routers.DefaultRouter()
router.register(r'product-category', views.ProductCategoryViewSet, basename='productcategory')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'product-review', views.ProductReviewViewSet, basename='product_review')
# SERVICES
router.register(r'service-category', views.ServiceCategoryViewSet, basename='servicecategory')
router.register(r'services', views.ServiceViewSet, basename='service')
router.register(r'service-review', views.ServiceReviewViewSet, basename='service_review')
urlpatterns += router.urls
