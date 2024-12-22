from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    
class Employee(models.Model):
    user = models.ForeignKey("accounts.user", on_delete=models.CASCADE)
    company = models.ForeignKey("companies.company", on_delete=models.CASCADE)
    