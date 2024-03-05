from django.db import models

# Create your models here.
from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
    full_name = models.CharField(max_length=60,blank=False,null=False)
    phone=models.CharField(max_length=13,blank=False,null=False,unique=True)
    dob=models.CharField(max_length=20,blank=False,null=False)
    email=models.EmailField(max_length=200,null=True,blank=True)
    gender=models.CharField(max_length=20,blank=False,null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    ROLE_CHOICES = (    
        ('admin', 'Admin'),
        ('customer','customer')
    )
    user_type = models.CharField(max_length=20,default='customer', choices=ROLE_CHOICES)
   

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.phone}{self.full_name}"

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='category',null=True,blank=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offerprice = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    quantity = models.PositiveIntegerField()
    is_out_of_stock = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='product_qrcodes', blank=True, null=True)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    def __str__(self):
        return f"{self.category.name} {self.name}"