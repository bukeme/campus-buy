from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import RegisterUserSerializer
from rest_framework.permissions import AllowAny

User = get_user_model()



class UserCreate(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterUserSerializer
	permission_classes = [AllowAny]

user_create = UserCreate.as_view()