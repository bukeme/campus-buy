from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAccountOwner(BasePermission):
	message = "You are not allowed to edit this profile"

	def has_object_permission(self, request, view, obj):
		if (not request.method in SAFE_METHODS) and (not request.user.is_authenticated):
			return False
		if request.method in ['PUT', 'DELETE']:
			return obj == request.user
		return True

class IsAccountConnectionOwner(BasePermission):
	message = "You are not allowed to edit this connection"

	def has_object_permission(self, request, view, obj):
		if request.method == 'PUT':
			return obj.user == request.user
		return True