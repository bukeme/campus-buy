from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Connection

User = get_user_model()


@receiver(post_save, sender=User)
def create_connection(sender, instance, created, *args, **kwargs):
	if created:
		Connection.objects.create(user=instance)