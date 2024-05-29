from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=30)
    category_image_path = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name +" "+ 'obj'
    
class Colors(models.Model):
    color = models.CharField(max_length=30)

    def __str__(self):
        return self.color
    

class Product(models.Model):

    DIM_CHOICES = {
        ('12x15','12X15'),
        ('12x18','12X18'),
        ('16x24','16X24'),
        ('12x8','12X8'),
        ('20x30','20X30'),
    }
    product_name = models.CharField(max_length=50)
    product_dim = models.CharField(max_length=20,choices=DIM_CHOICES)
    product_col = models.ManyToManyField(Colors)
    product_quantity = models.IntegerField()
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_price = models.IntegerField()
    product_image_path = models.CharField(max_length=100,default='images/product_imgs/.jpg')
    product_desc = models.TextField(default="Crafted with sleek sophistication, our frame seamlessly merges timeless design with modern functionality, ensuring your cherished memories are elegantly showcased in any setting")

    def __str__(self):
        return self.product_name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],default=1)

class Addresses(models.Model):
    name = models.CharField(max_length=50,default="")
    phone = models.CharField(max_length=20,default='')
    address = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    land_mark = models.CharField(max_length=50,default="")
    pincode = models.CharField(default='',max_length=10)

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order_date = models.DateTimeField(default=timezone.now)
    order_total = models.IntegerField()
    order_status = models.CharField(max_length=30)
    payment_order_id = models.CharField(max_length=100,null=True)
    order_address = models.TextField(null=True)
    razorpay_order_id = models.CharField(max_length=100,null=True)

class Order_items(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_price = models.IntegerField(null=True)
    product_quantity = models.IntegerField(null=True)


class Cart_total(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total_amount = models.IntegerField(default=0)

