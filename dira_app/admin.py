from django.contrib import admin
from . import models

# Register your models here.

models_list = [models.Farmer, models.Agrovet, models.Product, models.Diagnosis, models.Treatment, models.Order, models.Resource]

admin.site.register(models_list)
