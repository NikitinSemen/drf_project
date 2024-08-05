from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone


@shared_task
def filter_inactive_users():
    User = get_user_model()
    inactive_duration = timezone.timedelta(hours=24)
    inactive_users = User.objects.filter(last_login__lt=timezone.now() - inactive_duration, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()

    print(f"Deactivated {inactive_users.count()} users.")
