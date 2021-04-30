from django.db import models

# Create your models here.
class Block_printing(models.Model):
    question1 = models.CharField(max_length=500)
    answer1 = models.CharField(max_length=350)
    image1 = models.ImageField(upload_to='pics')
    question2 = models.CharField(max_length=500,default=None,null=True)
    answer2 = models.CharField(max_length=5000,default=None,null=True)
    image2 = models.ImageField(upload_to='pics',default=None,null=True)
    page_number = models.IntegerField(unique=True)