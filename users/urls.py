from django.urls import path
from . import views



urlpatterns = [
	path('create/', views.user_create, name='user_create'),
	path('list/', views.user_list, name='user_list'),
]