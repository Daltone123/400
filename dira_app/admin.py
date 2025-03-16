from django.contrib import admin
from . import models

# Register your models here.

models_list = [models.Farmer, models.Agrovet]

admin.site.register(models_list)
