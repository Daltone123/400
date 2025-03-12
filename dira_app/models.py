from django.db import models
from django.contrib.auth.models import User

class Farmer(models.Model):
  first_name = models.CharField(max_length=100, blank=False, null=False)
  last_name = models.CharField(max_length=100, blank=False, null=False)
  profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="farmer_profile", null=False)
  email = models.CharField(max_length=100, blank=False, null=False, unique=True)
  phone_number = models.CharField(max_length=100, blank=False, null=False, unique=True)
  farm_location = models.JSONField()
  farm_size = models.CharField(max_length=100, blank=False, null=False)
  type_of_crops = models.CharField(max_length=100, blank=False, null =False)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"


class Agrovet(models.Model):
  first_name = models.CharField(max_length=100, blank=False, null=False)
  last_name = models.CharField(max_length=100, blank=False, null=False)
  profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agrovet_profile", null=False)
  email = models.CharField(max_length=100, blank=False, null=False, unique=True)
  phone_number = models.CharField(max_length=100, blank=False, null=False, unique=True)
  agrovet_name = models.CharField(max_length=100, blank=False, null=False, unique=True)
  agrovet_location = models.JSONField()
  business_licence_number = models.CharField(max_length=100, blank=False, null=False, unique=True)
  
  def __str__(self):
    return self.agrovet_name