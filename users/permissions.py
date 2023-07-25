from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
	message = "You are not allowed to edit this profile"

	def has_object_permission(self, request, view, obj):
		if request.method == 'PUT':
			return obj == request.user
		return True

class IsAccountConnectionOwner(BasePermission):
	message = "You are not allowed to edit this connection"

	def has_object_permission(self, request, view, obj):
		if request.method == 'PUT':
			return obj.user == request.user
		return True