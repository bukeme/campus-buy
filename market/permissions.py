from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
	message = "You're only allowed to view categories"

	def has_permission(self, request, view):
		if (not request.method in SAFE_METHODS) and (not request.user.is_authenticated):
			return False
		if request.method in ['PUT', 'DELETE']:
			return request.user.is_staff
		return True

class IsProductOwnerOrReadOnly(BasePermission):
	message = "You're only allowed to view this product"

	def has_object_permission(self, request, view, obj):
		if (not request.method in SAFE_METHODS) and (not request.user.is_authenticated):
			return False
		if request.method in ['PUT', 'DELETE']:
			return request.user == obj.seller
		return True

class IsImageOwnerOrReadOnly(BasePermission):
	message = "You're only allowed to view this image"

	def has_object_permission(self, request, view, obj):
		if (not request.method in SAFE_METHODS) and (not request.user.is_authenticated):
			return False
		if request.method in ['PUT', 'DELETE']:
			return request.user == obj.product.seller
		return True

class IsProductReviewOwnerOrReadOnly(BasePermission):
	message = "You're only allowed to view this product"

	def has_object_permission(self, request, view, obj):
		if (not request.method in SAFE_METHODS) and (not request.user.is_authenticated):
			return False
		if request.method in ['PUT', 'DELETE']:
			return request.user == obj.user
		return True

class IsServiceImageOwnerOrReadOnly(BasePermission):
	message = "You're only allowed to view this image"

	def has_object_permission(self, request, view, obj):
		if (not request.method in SAFE_METHODS) and (not request.user.is_authenticated):
			return False
		if request.method in ['PUT', 'DELETE']:
			return request.user == obj.service.seller
		return True
