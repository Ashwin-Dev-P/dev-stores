from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class PaymentDetails_paytm(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    TXNID = models.CharField(max_length=500,unique=True)
    BANKTXNID = models.CharField(max_length=500)
    ORDERID = models.CharField(max_length=255)
    TXNAMOUNT = models.FloatField()
    STATUS = models.CharField(max_length=100)
    TXNTYPE = models.CharField(max_length=100)
    GATEWAYNAME = models.CharField(max_length=100)
    RESPCODE = models.CharField(max_length=100)
    RESPMSG = models.CharField(max_length= 100)
    BANKNAME = models.CharField(max_length = 255)
    MID = models.CharField(max_length = 500)
    PAYMENTMODE = models.CharField(max_length= 100)
    REFUNDAMT = models.FloatField()
    TXNDATE = models.CharField(max_length=100)
    
class PaymentDetails_razorpay(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=256,unique=True)
    
class PaymentDetails_paypal(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    orderID = models.CharField(max_length= 200)
    payerID = models.CharField(max_length= 200)
    paymentID = models.CharField(max_length= 500)
    billingToken = models.CharField(max_length= 500)
    facilitatorAccessToken = models.CharField(max_length= 500)