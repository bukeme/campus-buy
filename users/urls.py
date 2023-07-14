from django.urls import path
from . import views



urlpatterns = [
	path('create/', views.user_create, name='user_create'),
]