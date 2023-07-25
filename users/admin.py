from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import Connection

User = get_user_model()

# Register your models here.

class UserAdmin(BaseUserAdmin):
	form = UserAdminChangeForm
	add_form = UserAdminCreationForm

	list_display = ['email', 'first_name', 'last_name', 'reg_no', 'is_active', 'admin']
	list_filter = ['email', 'reg_no', 'is_active', 'admin']
	fieldsets = (
		(None, {'fields': ('email', 'reg_no')}),
		('Personal', {'fields': ('first_name', 'last_name', 'profile_image')}),
		('Student Info', {'fields': ('faculty', 'department', 'level', 'campus')}),
		('Permissions', {'fields': ('admin',)}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('first_name', 'last_name', 'reg_no', 'email', 'password', 'password_2')	
		}),
	)
	search_fields = ['email', 'reg_no']
	ordering = ['-date_joined']

admin.site.register(User, UserAdmin)

admin.site.register(Connection)
