from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self, first_name, last_name, email, username, password=None):
		if not email:
			raise ValueError('User must have an email address')

		email = self.normalize_email(email)

		user = self.model(
			first_name=first_name,
			last_name=last_name,
			email=email,
			username=username
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_staffuser(self, first_name, last_name, email, username, password):
		user = self.create_user(
			first_name=first_name,
			last_name=last_name,
			email=email,
			username=username,
			password=password
		)
		user.staff = True
		user.save(using=self._db)
		return user

	def create_superuser(self, first_name, last_name, email, username, password):
		user = self.create_user(
			first_name=first_name,
			last_name=last_name,
			email=email,
			username=username,
			password=password
		)
		user.staff = True
		user.admin = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True
	)
	first_name = models.CharField(max_length=150, blank=True)
	last_name = models.CharField(max_length=150, blank=True)
	username = models.CharField(max_length=150, unique=True)
	profile_image = models.ImageField(upload_to='profile_images/%Y-%m-%d', default='placeholder.jpg')
	is_active = models.BooleanField(default=True)
	staff = models.BooleanField(default=False)
	admin = models.BooleanField(default=False)
	date_joined = models.DateTimeField(default=timezone.now)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

	def get_full_name(self):
		return f'{(self.first_name).capitalize()} {(self.last_name).capitalize()}'

	def __str__(self):
		return self.username

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_superuser(self):
		return self.admin
	
	
