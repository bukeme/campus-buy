from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import RegisterUserSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

User = get_user_model()



class UserCreateAPIView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterUserSerializer
	permission_classes = [AllowAny]

user_create = UserCreateAPIView.as_view()

class UserListAPIView(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [IsAuthenticated]

user_list = UserListAPIView.as_view()