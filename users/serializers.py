from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['pk', 'first_name', 'last_name', 'profile_image', 'email', 'username', 'password']
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


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['pk', 'first_name', 'last_name', 'profile_image', 'email', 'username', 'password']
		extra_kwargs = {'password': {'write_only': True}, 'pk': {'read_only': True}}