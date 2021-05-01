from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import auth
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.http import HttpResponse
from .models import *
import os, sys
sys.path.insert(1, os.getcwd()) 
from ThumkiStores.models import *



from .utils import VerifyPaytmResponse
from django.conf import settings
from . import Checksum
from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_mail(cart_products,user_id,payment_id,request):
    try:
        subject = 'Thumki payment details'
        html_message = render_to_string('mail_template.html', {'cart_products': cart_products,'user_id':user_id,'payment_id':payment_id})
        plain_message = strip_tags(html_message)
        email_from = settings.EMAIL_HOST_USER
        to = User.objects.get(id=user_id).email
        try:
            mail.send_mail( subject, plain_message, email_from, [to], html_message=html_message )  
            messages.success(request,'Payment details have been sent to your mail')
        except:
            messages.info(request,"Mail not sent")
        
    except:
        messages.error(request,"Error sending mail")



def move_cart_to_orders(id,payment_id,request): 
    
    cart_products = Cart.objects.filter(user_id=id)
    
    try:
        for product in cart_products:
            product_id=product.product_id   
            size = product.size
            quantity = product.quantity
            user_id = id    
            
            product_sale_quantity_to_increase = Dress.objects.filter(id=product_id).first()
            product_sale_quantity_to_increase.sale_count = product_sale_quantity_to_increase.sale_count + quantity
            product_sale_quantity_to_increase.save()
            
            orders = Orders(product_id=product_id,size=size,quantity=quantity,user_id=id,payment_id=payment_id)
            orders.save()
    except:
        messages.error(request,"Error moving cart items to orders")

    try:
        Final_pay_amount = 0
        cart_items_list = []
        for items in cart_products:
            fetched_item = Dress.objects.filter(id=items.product_id).first()
            
            if(fetched_item.availability):
            
                data =  {  
                    'id' :  items.id ,
                    'name': fetched_item.name,
                    'size': items.size ,
                    'price': fetched_item.price ,
                    'quantity': items.quantity ,
                    'total': items.quantity * fetched_item.price  ,
                    'product_id': items.product_id ,
                    'img_url': fetched_item.img.url,
                    
                }    
                total_price =  data['price'] * data['quantity']
                Final_pay_amount = Final_pay_amount + total_price
                cart_items_list.append(data)
    except:
        messages.error(request,"Error gathering details about cart products for mail")

    send_mail(cart_items_list,id,payment_id,request)
    
    try:
        cart_products.delete()   
    except: 
        messages.error(request,"Unable to remove cart products")



def payment_success(request):
    
    if(request.user.is_authenticated):
        logged_in = True
        cart_item_quantity = len(Cart.objects.filter(user_id=request.user.id))
    else:
        logged_in = False
    
    mydata = General_info.objects.first()
    response = request.POST
    categories = Category.objects.all()
    
    
    
    if( 'razorpay_payment_id' in response ):
        razorpay_payment_id = response['razorpay_payment_id']
        
        if(PaymentDetails_razorpay.objects.filter(payment_id=razorpay_payment_id).exists()):
            messages.info(request,"Payment already done")
        else:
            try:
                payment_details = PaymentDetails_razorpay(user_id=request.user.id,payment_id=razorpay_payment_id)
                payment_details.save()
                messages.success(request,'Payment success')
                try:
                    move_cart_to_orders(request.user.id,razorpay_payment_id,request)
                except:
                    messages.error(request,"Unable to move cart items to orders")
                
            except:
                messages.error(request,'Error saving billing details to database.Please contact us.')
        
        
        
    
        
    else:
        messages.error(request,'Transaction failed')     
        return render(request,'payment_success.html',{'title':'Thumki','logged_in':logged_in,'cart_item_quantity':cart_item_quantity,'categories':categories,'mydata':mydata})
    
    
    
    cart_item_quantity = 0
    return render(request,'payment_success.html',{'title':'Thumki','logged_in':logged_in,'cart_item_quantity':cart_item_quantity,'categories':categories,'mydata':mydata})
        

def payment_paytm(request):
    order_id = Checksum.__id_generator__()
    
    cart_items = Cart.objects.filter(user_id=request.user.id)
    Final_pay_amount = 0
    for items in cart_items:
        fetched_item = Dress.objects.filter(id=items.product_id).first()
        
        if(fetched_item.availability):
        
            data =  {  
                'price': fetched_item.price ,
                'quantity': items.quantity ,
            }    
            total_price =  data['price'] * data['quantity']
            Final_pay_amount = Final_pay_amount + total_price
    Final_pay_amount = Final_pay_amount
    bill_amount = Final_pay_amount
    
    email = User.objects.filter(id=request.user.id).first().email
    
    
    
    data_dict = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
        'WEBSITE': settings.PAYTM_WEBSITE,
        'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
        'CALLBACK_URL': settings.PAYTM_CALLBACK_URL + str(request.user.id) ,
        
        'MOBILE_NO': '',
        'EMAIL': (email),
        'CUST_ID': str(request.user.id) ,
        
        'ORDER_ID':order_id,
        'TXN_AMOUNT': str(bill_amount),
    }
    data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
    context = {
        'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
        'comany_name': settings.PAYTM_COMPANY_NAME,
        'data_dict': data_dict
    }
    return render(request, 'payment/payment.html', context)

@csrf_exempt
def response(request,id):
    user = User.objects.filter(id=id).first()
    auth.login(request,user)
    
    resp = VerifyPaytmResponse(request)
    mydata = General_info.objects.first()
    if resp['verified']:
        
        if( PaymentDetails_paytm.objects.filter(TXNID=resp['paytm']['TXNID']).exists() ):
            messages.info(request,"Payment already done.")
        else:
            payment_details_form = PaymentDetails_paytm(
                user_id=id,
                TXNID=resp['paytm']['TXNID'],
                BANKTXNID=resp['paytm']['BANKTXNID'],
                ORDERID=resp['paytm']['ORDERID'],
                TXNAMOUNT=resp['paytm']['TXNAMOUNT'],
                STATUS=resp['paytm']['STATUS'],
                TXNTYPE=resp['paytm']['TXNTYPE'],
                GATEWAYNAME=resp['paytm']['GATEWAYNAME'],
                RESPCODE=resp['paytm']['RESPCODE'],
                RESPMSG=resp['paytm']['RESPMSG'],
                BANKNAME=resp['paytm']['BANKNAME'],
                MID=resp['paytm']['MID'] ,
                PAYMENTMODE=resp['paytm']['PAYMENTMODE'],
                REFUNDAMT=resp['paytm']['REFUNDAMT'],
                TXNDATE=resp['paytm']['TXNDATE']
            )
            
            
            try:
                payment_details_form.save()
                messages.success(request,"Transaction successful")
            except:
                messages.error(request,"Error saving the payment details to the database")
        
            payment_id=resp['paytm']['TXNID']
            move_cart_to_orders(id,payment_id)
            
            

        
        return render(request,'payment_success.html',{'title':'Thumki','mydata':mydata,'cart_item_quantity':0})
    else:
        messages.error(request,"Transaction failed")
        
        
        cart_item_quantity = len(Cart.objects.filter(user_id=id))
        return render(request,'payment_success.html',{'title':'Thumki','mydata':mydata,'cart_item_quantity':cart_item_quantity})


@csrf_exempt
def paypal_recieve(request):
    
    orderID =  request.POST['data[orderID]']
    
    payerID = request.POST['data[payerID]']
    paymentID = request.POST['data[paymentID]']
    billingToken =  request.POST['data[billingToken]']
    facilitatorAccessToken = request.POST['data[facilitatorAccessToken]']
    
    if(len(paymentID) < 1):
        payment_id = orderID
    
    details = PaymentDetails_paypal(orderID=orderID,payerID=payerID,paymentID=paymentID,billingToken=billingToken,facilitatorAccessToken=facilitatorAccessToken,user_id=request.user.id)
    details.save()
    
    move_cart_to_orders(request.user.id,payment_id)
    
    messages.success(request,"Payment success")
    messages.success(request,"Payment details have been sent to your email")
    return JsonResponse({
                'msgType': 'success',
                'msg': 'Payment Success'
            })
    
    
    
    