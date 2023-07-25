from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Connection

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['pk', 'first_name', 'last_name', 'reg_no', 'profile_image', 'email', 'password']
		extra_kwargs = {
			'password': {'write_only': True},
			'pk': {'read_only': True},
			'profile_image': {'read_only': True}
		}

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		instance = self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance

class UserConnectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Connection
		fields = ['pk', 'facebook', 'whatsapp', 'email', 'twitter', 'instagram', 'phone']


class UserSerializer(serializers.ModelSerializer):
	connection = UserConnectionSerializer(many=False, read_only=True)
	class Meta:
		model = User
		fields = ['pk', 'first_name', 'last_name', 'reg_no', 'faculty', 'department', 'level', 'campus', 'profile_image', 'email', 'password', 'connection']
		extra_kwargs = {'password': {'write_only': True}, 'pk': {'read_only': True}}