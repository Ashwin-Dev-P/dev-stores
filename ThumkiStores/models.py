  
from django.db import models
from django import forms
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User
import datetime


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='pics/categories')
    description = models.CharField(max_length=1000,default='Category descriptions')
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name
    
class Dress(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=4)
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    colour = models.CharField(max_length=255,default='black')
    sale_count = models.IntegerField(default=1)
    availability = models.BooleanField(default=True)
    material = models.CharField(max_length=255,default='cotton')
    additional_info = models.CharField(max_length=1500,default="Product description goes here.")
    
    class Meta:
        verbose_name_plural = "Dresses"
        
    def __str__(self):
        return self.name
    
class Customer_review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=500,default='')
    product = models.ForeignKey(Dress,default=None,on_delete=models.CASCADE,)
    review_title = models.CharField(max_length=500,default='My review')
    review = models.CharField(max_length=500)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    position = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Reviews"
        
    def __str__(self):
        return self.review
       
class Messages(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(default=None)
    phone_number = models.CharField(max_length=20,default=None)
    message = models.CharField(max_length=500)
    read = models.BooleanField(default=False)
    date = models.DateField( default=datetime.date.today)
    
    class Meta:
        verbose_name_plural = "Messages"
        
    def __str__(self):
        return self.message
    
class FAQ(models.Model):
    
    question = models.CharField(max_length=2000)
    answer = models.CharField(max_length=10000)
    
    class Meta:
        verbose_name_plural = "FAQ"
        
    def __str__(self):
        return self.question
    
class Subscription(models.Model):
    name=models.CharField(max_length=100)
    email = models.EmailField(max_length=256,unique=True)
    
    class Meta:
        verbose_name_plural = "Subscriptions"
        
    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    product = models.ForeignKey(Dress,default=None,on_delete=models.CASCADE,)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    size = models.CharField(default=None,max_length=20)
    
class Sizes(models.Model):
    product = models.ForeignKey(Dress,on_delete=models.CASCADE,default=1)
    extra_small = models.BooleanField(default=True)
    small = models.BooleanField(default=True)
    medium = models.BooleanField(default=True)
    large = models.BooleanField(default=True)
    extra_large = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Sizes"
        
    def __str__(self):
        return str(self.product_id)
    
class Orders(models.Model):
    payment_id = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    product = models.ForeignKey(Dress,default=None,on_delete=models.CASCADE,)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    size = models.CharField(default=None,max_length=20)
    date = models.DateField( default=datetime.date.today)
    delivered = models.BooleanField(default=False)
    
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1,unique=True)
    phone_number = models.CharField(max_length=20,default=None)
    address = models.CharField(max_length=500,null=False)
    
    class Meta:
        verbose_name_plural = "User Profile"
        
    def __str__(self):
        return str(self.user)

class General_info(models.Model):
    store_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='pics')
    fav_icon = models.ImageField(upload_to='pics')
    year = models.IntegerField()
    instagram_link = models.CharField(max_length=500)
    facebook_link = models.CharField(max_length=500)
    email_id = models.EmailField(max_length=256) 
    email_password = models.CharField(max_length=256)
    whatsapp_number = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Store Details"
        
    def __str__(self):
        return self.store_name   
    