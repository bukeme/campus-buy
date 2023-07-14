from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

# Register your models here.

class UserAdmin(BaseUserAdmin):
	form = UserAdminChangeForm
	add_form = UserAdminCreationForm

	list_display = ['email', 'username', 'first_name', 'last_name', 'is_active', 'admin']
	list_filter = ['email', 'username', 'is_active', 'admin']
	fieldsets = (
		(None, {'fields': ('email', 'username')}),
		('Personal', {'fields': ('first_name', 'last_name', 'profile_image')}),
		('Permissions', {'fields': ('admin',)}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('first_name', 'last_name', 'email', 'username', 'password', 'password_2')	
		}),
	)
	search_fields = ['email', 'username']
	ordering = ['-date_joined']

admin.site.register(User, UserAdmin)
