from django.db import models
from django.contrib.auth.models import AbstractUser

# Extend Django's default User model
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('farmer', 'Farmer'),
        ('agrovet', 'Agrovet'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    # Add related_name to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username


# Farmer model linked to CustomUser
class Farmer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="farmer_profile")
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.CharField(max_length=100, blank=False, null=False, unique=True)
    phone_number = models.CharField(max_length=100, blank=False, null=False, unique=True)
    farm_location = models.JSONField()
    farm_size = models.CharField(max_length=100, blank=False, null=False)
    type_of_crops = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Agrovet model linked to CustomUser
class Agrovet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="agrovet_profile")
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.CharField(max_length=100, blank=False, null=False, unique=True)
    phone_number = models.CharField(max_length=100, blank=False, null=False, unique=True)
    agrovet_name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    agrovet_location = models.JSONField()
    business_licence_number = models.CharField(max_length=100, blank=False, null=False, unique=True)
    
    def __str__(self):
        return self.agrovet_name


# ✅ Product Model linked to Agrovet
class Product(models.Model):
    agrovet = models.ForeignKey(Agrovet, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.agrovet.agrovet_name}"

    def is_low_stock(self):
        return self.stock_quantity < 10


# ✅ Order Model linked to Agrovet and Farmer
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    agrovet = models.ForeignKey(Agrovet, on_delete=models.CASCADE, related_name="orders")
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.status}"
