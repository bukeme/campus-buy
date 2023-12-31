from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response 
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterUserSerializer, UserSerializer, UserConnectionSerializer
from .permissions import IsAccountOwner, IsAccountConnectionOwner
from .models import Connection
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import QueryDict

User = get_user_model()



class UserCreateAPIView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterUserSerializer
	permission_classes = [AllowAny]

user_create = UserCreateAPIView.as_view()

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [IsAccountOwner]
	parser_classes = [MultiPartParser, FormParser]
	
user_list_viewset = UserViewSet.as_view({'get': 'list'})
user_detail_viewset = UserViewSet.as_view({'get': 'retrieve'})
user_update_viewset = UserViewSet.as_view({'put': 'update'})

class UserDetailAPIView(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		user = request.user
		serializer = UserSerializer(user, many=False)
		return Response(serializer.data)

user_detail = UserDetailAPIView.as_view()

class UserConnectionUpdateAPIView(generics.UpdateAPIView):
	queryset = Connection.objects.all()
	serializer_class = UserConnectionSerializer
	permission_classes = [IsAuthenticated, IsAccountConnectionOwner]

user_connection_update = UserConnectionUpdateAPIView.as_view()