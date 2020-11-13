from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")
    name = models.TextField(unique=True)

    email = models.TextField(null=True)
    backup_email = models.TextField(null=True)
    phone = models.CharField(null=True, max_length=11)
    backup_phone = models.CharField(null=True, max_length=11)
    remark = models.TextField(null=True)

    last_login_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
