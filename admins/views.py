from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth
import os, sys
sys.path.insert(1, os.getcwd()) 
from ThumkiStores.models import *


mydata={
    
    'year': '2021',
    'store_name' : "Thumki"
}


# Create your views here.
def admins_login(request):
    if(request.method == 'POST'):
        username = request.POST.get('username','')
        if(len(username) < 1 ):
            messages.error(request,"Enter your username")
            return redirect('admins_login')
        password = request.POST.get('password','')
        if(len(password) < 1 ):
            messages.error(request,"Enter your password")
            return redirect('admins_login')
        
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            if user.is_superuser:
                messages.success(request,'Logged in successfully.')
                auth.login(request,user)
                return redirect('orders',delivered =0)
            else:
                messages.error(request,'Your account is not an admin account')
                return redirect('admins_login')
        else:
            messages.error(request,'Invalid credentials.')
            return redirect('admins_login')
    return render(request,"admins/login.html")
            

    
    

def orders(request,delivered):
    if(request.user.is_authenticated):
    
        if(request.user.is_superuser): 
            delivered_int = delivered
            if(delivered == 1):
                delivered = True
            else:
                delivered = False
            unique_payment_ids = Orders.objects.values('payment_id').distinct().filter(delivered=delivered).order_by('date')
            orders_list = []
            for payment_id in unique_payment_ids: 
                order = Orders.objects.filter(payment_id=payment_id['payment_id'],delivered=delivered).first()
                
                
                user_id = order.user_id
                
                user = User.objects.filter(id=user_id).first()
                
                try:
                    first_name = user.first_name
                    last_name = user.last_name
                    name = first_name + last_name
                except:
                    name = user
                if(len(name) < 1):
                    name = user
                
                    
                date = order.date
                order_id =order.id
                data = {
                    'name': name,
                    'date': date,
                    'payment_id':payment_id['payment_id']
                }        
                orders_list.append(data)
            return render(request,'admins/orders.html',{'orders_list':orders_list,'delivered':delivered})
        else:
            messages.error(request,"Only admins can access the page")
            return redirect('admins_login')

    else:
        messages.error(request,"Login to continue")
        return redirect('admins_login')


def orders_info(request,payment_id):
    if(request.user.is_authenticated):
        
        if(request.user.is_superuser):
            if(Orders.objects.filter(payment_id=payment_id).exists()):
                if(request.method == 'GET'):
                    Total_amount = 0
                    orders = Orders.objects.filter(payment_id=payment_id)
                    user_id = orders.first().user_id
                    
                    
                    customer = User.objects.get(id=user_id)
                    profile = Profile.objects.get(user_id=user_id)
                    
                    
                    
                    
                    
                    delivered= orders.first().delivered
                    
                    products_list = []
                    for order in orders:
                        product_id = order.product_id
                        product = Dress.objects.get(id=product_id)
                        data = {
                            'id': product_id,
                            'name': product.name,
                            'quantity': order.quantity,
                            'size': order.size,
                            'price': product.price,
                            'img': product.img,
                            
                            
                            
                        }
                        products_list.append(data)
                        Total_amount = Total_amount + (  float(data['price']) * float(data['quantity']) )
                        date = orders.first().date
                        
                    return render(request,'admins/orders_info.html',{ 'product_list':products_list,'Total_amount':Total_amount,'customer':customer,'payment_id':payment_id,'date':date,'delivered':delivered,'profile':profile })
            
                elif(request.method == 'POST'):
                    orders = Orders.objects.filter(payment_id=payment_id)
                    for order in orders:
                        
                        if('delivered' in request.POST ):
                            order.delivered = True
                        elif('undeliver' in request.POST ):
                            order.delivered = False
                        order.save()
                    return redirect('orders',delivered=0)
                else:       
                    messages.error(request,"Only post and Get request methods will be handled.")
                    return render(request,'admins/orders_info.html',{ 'product_list':products_list,'Total_amount':Total_amount,'customer':customer,'payment_id':payment_id,'date':date,'delivered':delivered })
        else:
            messages.error(request,"Only admins can access the page")
            return redirect('admins_login')
    else:
        messages.error(request,"Login to continue")
        return redirect('admins_login')
    
def messages_recieved_func(request,read):
    if(request.user.is_authenticated):
        if(request.user.is_superuser):
            if(request.method == 'GET'):
                if(read == 0):
                    read = False
                else:
                    read = True
                    
                messages_recieved = Messages.objects.filter(read=read)
                message_count = len(messages_recieved)
                return render(request,"admins/messages.html",{'mydata':mydata,'messages_recieved':messages_recieved,'message_count':message_count,'read':read })
            elif(request.method == 'POST'):
                message_id = request.POST.get('message_id',0)
                selected_message = Messages.objects.get(id=message_id)
                selected_message.read = True
                selected_message.save()
                
                messages.success(request,"Marked as read")
                return redirect('messages_recieved_func',0)

        else:
            messages.error(request,"Only admins can access the page")
            return redirect('admins_login')
    else:
        messages.error(request,"Login to continue")
        return redirect('admins_login')
    
    
def subscribed_customers(request):
    subscribed_accounts = Subscription.objects.all()
    return render(request,"admins/subscribed_customers.html",{'subscribed_accounts':subscribed_accounts })
    
    
    


def admins_log_out(request):
    auth.logout(request)
    return redirect('admins_login')
            
    
 
    
    
    
    