from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Permission

from companies.models import Company

class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_owner = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.email
    
class Group(models.Model):
    name = models.CharField(max_length=80)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
class Group_Permission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
class User_Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    
