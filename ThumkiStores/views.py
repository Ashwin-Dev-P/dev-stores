from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import auth,User
import json
from .models import *
from django.http import JsonResponse
from django.http import HttpResponseRedirect
import os, sys
sys.path.insert(1, os.getcwd()) 
from pages.models import *


top_n_sales = 3

mydata = General_info.objects.first()
 




def index(request):
      
    if(request.method == 'GET' ):
        top_sales_dress = Dress.objects.all().order_by('-sale_count')[:top_n_sales]
        
        categories = Category.objects.all()
        
        Reviews = Customer_review.objects.all()
        Review1 = Reviews.filter(position=1).first()
        Review2 = Reviews.filter(position=2).first()
        Review3 = Reviews.filter(position=3).first()
        Review4 = Reviews.filter(position=4).first()
        Review5 = Reviews.filter(position=5).first()
        
        Review = {
            'Review1': Review1 ,
            'Review2': Review2 ,
            'Review3': Review3 ,
            'Review4': Review4 ,
            'Review5': Review5 ,
        }
        
        info = Block_printing.objects.all()
        info1 = info.get(page_number=1)
        info2 = info.get(page_number=2)
        
        
        cart_item_quantity = len(Cart.objects.filter(user_id=request.user.id) )
        
        if(request.user.is_authenticated):
            logged_in = True
        else:
            logged_in = False
            
        
        mydata = General_info.objects.first()
        return render(request,"index.html",{'title':'Thumki','logged_in':logged_in,'categories':categories,'top_sales_dress':top_sales_dress,'mydata':mydata,'cart_item_quantity':cart_item_quantity,'info2':info2,'info1':info1,'Review':Review})

def shop(request):
    info = Block_printing.objects.all()
    info1 = info.get(page_number=1)
    info2 = info.get(page_number=2)
    if(request.method == 'GET' ):
        
        
        category_id = request.GET.get('category_id',0)
        
        if(category_id == 0):
            dresses  = Dress.objects.all().order_by('id') 
        else:
            dresses = Dress.objects.filter(category_id=category_id).order_by('id') 
        
        
        cart_item_quantity = len(Cart.objects.filter(user_id=request.user.id) )
        if(len(dresses) == 0 ):
            messages.error(request,'No products available')
            
            mydata = General_info.objects.first()
            categories = Category.objects.all()
            return render(request,"error.html",{'title':'Error','mydata':mydata,'cart_item_quantity':cart_item_quantity,'info2':info2,'info1':info,'categories':categories})
        
        items_per_row = 3
        rows_per_page = 2
        items_per_page = items_per_row * rows_per_page
        
        
        total_pages = len(dresses) /items_per_page
        
        page_number = int(request.GET.get('pg', 1))
        
        previous_page_number = 0
        next_page_number = 0
        if(not (page_number < 2)):
            previous_page_number = int(request.GET.get('pg', 1)) - 1
            
        if(total_pages > page_number):
            next_page_number = int(request.GET.get('pg', 1)) + 1
            
        starting = ( page_number * items_per_page   )  - items_per_page
        ending   = ( page_number * items_per_page   )
        dresses  = dresses[starting:ending]
        
        categories = Category.objects.all()
                
        mydata = General_info.objects.first()
        return render(request,"shop.html",{'title':'Shop','dresses':dresses,'mydata':mydata,'current_page':page_number,'cart_item_quantity':cart_item_quantity,'categories':categories,'previous_page_number':previous_page_number,'next_page_number':next_page_number,'page_number':page_number,'info2':info2,'info1':info1})

def viewtest(request):
    if(request.method == 'POST' ):
        if('product_id' in request.POST):
            product_id = request.POST['product_id']
            s = Customer_review.objects.filter(product_id=product_id).filter(user_id=request.user.id)
        else:
            return JsonResponse({
                'msgType': 'error',
                'msg': 'There is an error accessing this product.'
            })
            
        if(s.exists()):
            return JsonResponse({
                'msgType': 'info',
                'msg': 'You have entered your review for this product already.'
            })
        
    
        name = str(request.POST.get('name',''))
        if(len(name) < 1):
            messages.error(request,"Enter your name")
            return JsonResponse({
                'msgType': 'error',
                'msg': 'Enter your name.'
            })
        
            
        rating = int(request.POST.get('rating',5))
        if(rating < 1 or rating > 5):
            messages.error(request,"Enter a valid rating")
            return JsonResponse({
                'msgType': 'error',
                'msg': 'Enter the rating.'
            })
        
        review_title = request.POST.get('review_title','')
        if(len(review_title) < 1):
            messages.error(request,"Enter your review title.")
            return JsonResponse({
                'msgType': 'error',
                'msg': 'Enter the review title.'
            })
        
        review = request.POST.get('customerreview','')
        if(len(review) < 1):
            messages.error(request,"Enter your review.")
            return JsonResponse({
                'msgType': 'error',
                'msg': 'Enter your review.'
            })
            
        form = Customer_review(rating=rating,review=review,product_id=product_id,review_title=review_title,name=name,user_id=request.user.id)
        form.save()
        return JsonResponse({
            'msgType': 'success',
            'msg': 'Review submitted'
        })
        
    


def view(request,id):
    info = Block_printing.objects.all()
    info1 = info.get(page_number=1)
    info2 = info.get(page_number=2)
    cart_item_quantity = len(Cart.objects.all())
    if( request.user.is_authenticated ):
        logged_in = True
    else:
        logged_in = False

    
    if(Dress.objects.filter(id=id).exists()):
        current_dress = Dress.objects.filter(id=id).first()
        category_name = Category.objects.get(id=current_dress.category_id).name
    else:
        messages.error(request, 'The item that you are requesting is not available.')
        mydata = General_info.objects.all().first()
        return render(request,"error.html",{'title':'error','mydata':mydata,'cart_item_quantity':cart_item_quantity,'mydata':mydata,'info2':info2,'info1':info1});
    reviews = Customer_review.objects.filter(product_id=id).all()
    top_sales_dress = Dress.objects.all().order_by('-sale_count')[:top_n_sales]
    
    
    customer_review_for_current_product = Customer_review.objects.filter(user_id=request.user.id,product_id=id) 
    if(customer_review_for_current_product.exists()):
        review_given = True
    else:
        review_given = False
    
    
    cart_item_quantity = len(Cart.objects.filter(user_id=request.user.id) )
    categories = Category.objects.all()
    if(request.method == 'GET' ):
        
        try:
            size_found = True
            sizes = Sizes.objects.get(product_id=id)
        except:
            size_found = False
            sizes = {}
            
        mydata = General_info.objects.first()
        return render(request,'view.html',{'title':'views','review_given':review_given ,'logged_in' : logged_in,'dress':current_dress,'reviews':reviews,'top_sales_dress':top_sales_dress,'mydata':mydata,'cart_item_quantity':cart_item_quantity,'category_name':category_name,'categories':categories,'info2':info2,'info1':info1,'size_found':size_found,'sizes':sizes })
    elif(request.method == 'POST' ):
        if(not logged_in):
            messages.error(request,"Login to continue")
            return redirect("login")
            
        if 'add_to_cart' in request.POST:
            if(Dress.objects.filter(id=id,availability=False).exists()):
                messages.error(request,"Product is out of stock.Cannot add to cart.")
                return redirect('view',id)
            
            
            quantity = request.POST.get('quantity',1)
            
            if('size' in request.POST):
                size = request.POST['size']
                if(len(size) < 1):
                    messages.error(request,"Select the product size.")
                    return redirect('view',id)
            else:
                messages.error(request,"Select the product size.")
                return redirect('view',id)
            
            same_product = Cart.objects.filter(user_id=request.user.id,product_id=id,size=size)
            if(same_product.exists()):
                same_product = Cart.objects.filter(user_id=request.user.id,product_id=id,size=size).first()
                same_product.quantity = int(quantity) + int(same_product.quantity);
                messages.success(request,"Quantity is incresed for this product in the cart.")
                same_product.save()
                return redirect('view',id)
                
            
            add_to_cart_form = Cart(user_id=request.user.id,product_id=id,size=size,quantity=quantity)
            try:
                add_to_cart_form.save()
            except:
                messages.error(request,"Error occured adding to the cart.")
                return redirect('view',id)

            messages.success(request,"Added to cart")
            cart_item_quantity = len(Cart.objects.filter(user_id=request.user.id) )
            return redirect('view',id)
    else:
        categories = Category.objects.all()
        messages.error(request, 'Not able to handle the method ',request.method,' .Only post and get requests will be handled.')
                            
        mydata = General_info.objects.first()
        return render(request,"error.html",{'title':'error','review_given':review_given,'mydata':mydata,'cart_item_quantity':cart_item_quantity,'categories':categories ,'info2':info2,'info1':info1}); 
    
    
def contact_us(request):
    info = Block_printing.objects.all()
    info1 = info.get(page_number=1)
    info2 = info.get(page_number=2)
    
    categories = Category.objects.all()
    cart_item_quantity = len(Cart.objects.filter(user_id=request.user.id) )
    if(request.method == 'GET'):
        mydata = General_info.objects.first()
        return render(request,'contact_us.html',{'title':'Contact Us','mydata':mydata,'cart_item_quantity':cart_item_quantity,'categories':categories })
    elif(request.method == 'POST'):
        
        name=request.POST['username']
        if(len(name) < 1):
            messages.error(request,"Enter your name")
            return redirect('contact_us')

        
        email = request.POST['email']
        if(len(email) < 5 ):
            messages.error(request,"Enter a valid email.")
            return redirect('contact_us')
        
        phone_number = request.POST['phone-number']
        
        message = request.POST['message']
        if(len(message) < 1):
            messages.error(request,"Enter a message.")
            return redirect('contact_us')
        
        
        message_form = Messages(name=name,email=email,phone_number=phone_number,message=message)
        try:
            message_form.save()
        except:
            messages.error(request,"Invalid form data.")
            return render(request,'contact_us.html',{'title':'Contact Us','mydata':mydata,'cart_item_quantity':cart_item_quantity,'info2':info2,'info1':info1})
        messages.success(request,"Message sent successfully.")
        return redirect('contact_us')
    else: 
        messages.error(request,'This request method cannot be handled.')
        mydata = General_info.objects.first()
        return render(request,"error.html",{'title':'error','mydata':mydata,'cart_item_quantity':cart_item_quantity,'info2':info2,'info1':info1});
    
def Subscribe(request):
    info = Block_printing.objects.all()
    info1 = info.get(page_number=1)
    info2 = info.get(page_number=2)
    
    cart_item_quantity = len(Cart.objects.filter(user_id=request.user.id) )
    if(request.method == 'GET'):
        categories = Category.objects.all()
        if(request.user.is_authenticated):
            logged_in = True
        else:
            logged_in = False
        mydata = General_info.objects.first()
        return render(request,'subscribe.html',{'title':'Subscribe','mydata':mydata,'cart_item_quantity':cart_item_quantity,'categories':categories,'info2':info2,'info1':info1})
    elif(request.method == 'POST'):
        
        email = request.POST.get('email','')        
        if(len(email) < 5 ):
            messages.error(request,"Enter a valid email.")
            mydata = General_info.objects.first()
            return render(request,'subscribe.html',{'title':'Subscribe','mydata':mydata,'cart_item_quantity':cart_item_quantity,'info2':info2,'info1':info1})
        if(Subscription.objects.filter(email=email).exists()):
            messages.info(request,"This email id has already been subscribed.")
            return redirect('Subscribe')
        
        
        name = request.POST.get('name','')
        if(len(name) < 1):
            messages.error(request,"Enter a valid name.")
            return redirect('Subscribe')
        
        subscription_form = Subscription(name=name,email=email)
        
        try:
            subscription_form.save()
            messages.success(request,"Subscribed.")
        except:
            messages.error(request,"Invalid form data.")
            return redirect('Subscribe')
        
        return redirect('Subscribe')
    else:
        messages.error(request, 'Not able to handle the method ',request.method,' .Only post and get requests will be handled.')
        return redirect('Subscribe')
        


def FAQ_page(request):
    info = Block_printing.objects.all()
    info1 = info.get(page_number=1)
    info2 = info.get(page_number=2)
    
    categories = Category.objects.all()
    cart_item_quantity = len(Cart.objects.filter(user_id=request.user.id) )
    if(request.method == 'GET'):
        if(request.user.is_authenticated):
            logged_in = True
        else:
            logged_in = False

        faq = FAQ.objects.all()
        mydata = General_info.objects.first()
        return render(request,'FAQ.html',{'title':'FAQ','logged_in':logged_in,'mydata':mydata,'faq':faq,'cart_item_quantity':cart_item_quantity,'categories':categories,'info2':info2,'info1':info1})    
    else:
        messages.error(request, 'Not able to handle the method ',request.method,' .Only post and get requests will be handled.')
        mydata = General_info.objects.first()
        return render(request,"error.html",{'title':'error','logged_in':logged_in,'mydata':mydata,'cart_item_quantity':cart_item_quantity,'info2':info2,'info1':info1}); 
    

def cart(request):
    info = Block_printing.objects.all()
    info1 = info.get(page_number=1)
    info2 = info.get(page_number=2)
    
    if(not request.user.is_authenticated ):
        messages.error(request,"Login to continue")
        return redirect('login')
    
    cart_items = Cart.objects.filter(user_id=request.user.id).order_by('id')
    
    cart_items_list = []
    Final_pay_amount = 0
    for items in cart_items:
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
    cart_item_quantity = len( cart_items_list )
    Final_pay_amount = Final_pay_amount
    categories = Category.objects.all()
    mydata = General_info.objects.first()
    return render(request,"cart.html",{'title':'Cart','Final_pay_amount':Final_pay_amount,'mydata':mydata,'cart_item_quantity':cart_item_quantity,'cart_items_list':cart_items_list,'categories':categories,'info2':info2,'info1':info1}); 

def cart_remove(request):
    
    item_id = request.GET['item_id']
    if(Cart.objects.filter(id=item_id).exists()):
        Cart.objects.filter(id=item_id).delete()
        messages.success(request,"Product removed from the cart")
    else:
        messages.error(request,"Product not found in the cart")
    return redirect('cart')

def cart_add_quantity(request):
    item_id = request.GET['item_id']
    if(Cart.objects.filter(id=item_id).exists()):
        current_item = Cart.objects.filter(id=item_id).first()
        current_item.quantity = current_item.quantity + 1
        current_item.save()
        messages.success(request,"Product quantity increased")
    else:
        messages.error(request,"Product not found in the cart")        
    return redirect('cart')

def cart_subtract_quantity(request):
    
    item_id = request.GET['item_id']
    if(Cart.objects.filter(id=item_id).exists()):
        current_item = Cart.objects.filter(id=item_id).first()
        if(current_item.quantity == 1):
            current_item.delete()
            messages.success(request,"Product removed from the cart")
        else:
            current_item.quantity = current_item.quantity - 1
            current_item.save()
            messages.success(request,"Product quantity decreased")
    else:
        messages.error(request,"Product not found in the cart")        
    return redirect('cart')


def reviews(request):
    info = Block_printing.objects.all()
    info1 = info.get(page_number=1)
    info2 = info.get(page_number=2)
    
    if(request.method == 'GET'):
        if(request.user.is_authenticated):
            logged_in = True
        else:
            logged_in = False
            
        reviews = Customer_review.objects.all()
        
        
        
        items_per_row = 3
        rows_per_page = 2
        items_per_page = items_per_row * rows_per_page
        
        
        total_pages = len(reviews) /items_per_page
        
        page_number = int(request.GET.get('pg', 1))
        
        previous_page_number = 0
        next_page_number = 0
        if(not (page_number < 2)):
            previous_page_number = int(request.GET.get('pg', 1)) - 1
            
        if(total_pages > page_number):
            next_page_number = int(request.GET.get('pg', 1)) + 1
            
        starting = ( page_number * items_per_page   )  - items_per_page
        ending   = ( page_number * items_per_page   )
        reviews  = reviews[starting:ending]
        
        
        
        
        categories = Category.objects.all()
        cart_item_quantity =len( Cart.objects.filter(user_id=request.user.id) )
        mydata = General_info.objects.first()
        return render(request,"reviews.html",{'title':'Reviews','logged_in':logged_in,'mydata':mydata,'cart_item_quantity':cart_item_quantity,'categories':categories,'reviews':reviews,'page_number':page_number,'next_page_number':next_page_number,'previous_page_number':previous_page_number,'info2':info2,'info1':info1 })

def profile(request,edit):
    info = Block_printing.objects.all()
    info1 = info.get(page_number=1)
    info2 = info.get(page_number=2)
    
    if(request.user.is_authenticated):
        if(request.method == 'GET'):
            if(edit == 0):
                edit = False
            else:
                edit = True
            user_details = User.objects.get(id=request.user.id)
            user_profile = Profile.objects.filter(user_id=request.user.id).first()  
            cart_item_quantity = len(Cart.objects.filter(user_id=request.user.id) )
            categories = Category.objects.all()
            mydata = General_info.objects.first()
            return render(request,'profile.html',{'title': 'profile' ,'mydata':mydata, 'user_details':user_details,'user_profile':user_profile,'edit':edit,'cart_item_quantity':cart_item_quantity,'categories':categories ,'info2':info2,'info1':info1})  
        elif(request.method == 'POST'):
            
            username = request.POST.get('username','')
            if(len(username) < 1):
                messages.error(request,"Enter your username")
                return redirect('profile',1)
              
            
            if( User.objects.filter(username=username).exists() ):
                another_user_of_same_username = User.objects.filter(username=username).first()
                check_id = another_user_of_same_username.id
                if( another_user_of_same_username and (request.user.id != check_id) ):
                    messages.error(request,"Username is taken")
                    return redirect('profile',1)
            
            
            address = request.POST.get('address','')
            if(len(address) < 1):
                messages.error(request,"Enter your address")
                return redirect('profile',1)
            
            
            email = request.POST.get('email','')
            phone_number = request.POST.get('phone_number','')
            if(len(email) < 5 and len(phone_number) < 9):
                messages.error(request,"Either your email or your phone number must be entered")
                return redirect('profile',1)
            
            
            
            first_name= request.POST.get('first_name','')
            last_name= request.POST.get('last_name','')
            
            
            user_object = User.objects.get(id=request.user.id)
            user_object.username = username
            user_object.first_name = first_name
            user_object.last_name = last_name
            user_object.email = email
            user_object.save()
            
            if(Profile.objects.filter(user_id=request.user.id).exists()):
                profile = Profile.objects.get(user_id=request.user.id)
                profile.address = address
                profile.phone_number = phone_number
                profile.save()
            else:
                profile_form = Profile(address=address,phone_number=phone_number)
                profile_form.save()               
                
                
            messages.success(request,"Profile updated")
            return redirect('profile',0)
        else:
            messages.error(request,"Only post and request data will be handled.")
    else:
        return redirect('login')
    
def confirm_details(request,edit):
    info = Block_printing.objects.all()
    info1 = info.get(page_number=1)
    info2 = info.get(page_number=2)
    
    if(request.user.is_authenticated):
        if(request.method == 'GET'):
            if(edit == 0):
                edit = False
            else:
                edit = True
            user_details = User.objects.get(id=request.user.id)
            user_profile = Profile.objects.filter(user_id=request.user.id).first()  
            cart_item_quantity = len(Cart.objects.filter(user_id=request.user.id) )
            categories = Category.objects.all()
            mydata = General_info.objects.first()
            return render(request,'confirm_details.html',{'title': 'profile' ,'mydata':mydata, 'user_details':user_details,'user_profile':user_profile,'edit':edit,'cart_item_quantity':cart_item_quantity,'categories':categories,'info2':info2,'info1':info1})  
        elif(request.method == 'POST'):
            
            username = request.POST.get('username','')
            if(len(username) < 1):
                messages.error(request,"Enter your username")
                return redirect('confirm_details',1)
              
            
            if( User.objects.filter(username=username).exists() ):
                another_user_of_same_username = User.objects.filter(username=username).first()
                check_id = another_user_of_same_username.id
                if( another_user_of_same_username and (request.user.id != check_id) ):
                    messages.error(request,"Username is taken")
                    return redirect('confirm_details',1)
            
            
            address = request.POST.get('address','')
            if(len(address) < 1):
                messages.error(request,"Enter your address")
                return redirect('confirm_details',1)
            
          
            email = request.POST.get('email','')
            phone_number = request.POST.get('phone_number','')
            if(len(email) < 5 and len(phone_number) < 9):
                messages.error(request,"Either your email or your phone number must be entered")
                return redirect('confirm_details',1)
            
            
          
            first_name= request.POST.get('first_name','')
            last_name= request.POST.get('last_name','')
            
            
            user_object = User.objects.get(id=request.user.id)
            user_object.username = username
            user_object.first_name = first_name
            user_object.last_name = last_name
            user_object.email = email
            user_object.save()
            
            if(Profile.objects.filter(user_id=request.user.id).exists()):
                profile = Profile.objects.get(user_id=request.user.id)
                profile.address = address
                profile.phone_number = phone_number
                profile.save()
            else:
                profile_form = Profile(address=address,phone_number=phone_number)
                profile_form.save()               
                
                
            messages.success(request,"Profile updated")
            return redirect('confirm_details',0)
        else:
            messages.error(request,"Only post and request data will be handled.")
    else:
        return redirect('login')

    
def payment_selection(request):
    info = Block_printing.objects.all()
    info1 = info.get(page_number=1)
    info2 = info.get(page_number=2)
    
    if(request.user.is_authenticated):
        if(request.method == 'GET'):
            if( Profile.objects.filter(user_id=request.user.id).exists() ):
                
                address = Profile.objects.get(user_id=request.user.id).address
                phone_number = Profile.objects.get(user_id=request.user.id).phone_number
                if( len(address) < 1 or len(str(phone_number)) < 10 ):
                    messages.error(request,'Both phone number and address is required to complete the payment')
                    return redirect('confirm_details',1)
                
                
                cart_items = Cart.objects.filter(user_id=request.user.id).order_by('id')
        
                cart_item_quantity = 0
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
                        cart_item_quantity = cart_item_quantity + 1;
                
                Final_pay_amount = Final_pay_amount
                Final_pay_amount_for_razorpay = Final_pay_amount * 100
                
               
                url = 'https://free.currconv.com/api/v7/convert?q=USD_INR&compact=ultra&apiKey=24e1586b2354cb6175ed'
                response = requests.get(url)
                data = json.loads(response.text)
                value= data['USD_INR']
                paypal_amount = float(Final_pay_amount / value)
                paypal_amount = round(paypal_amount,2)
                
                
                
                categories = Category.objects.all()
                mydata = General_info.objects.first()
                return render(request,'payment_selection.html',{'title':'payment_selection','Final_pay_amount':Final_pay_amount,'cart_item_quantity':cart_item_quantity,'Final_pay_amount_for_razorpay':Final_pay_amount_for_razorpay,'paypal_amount':paypal_amount,'categories':categories,'mydata':mydata ,'info2':info2,'info1':info1 })
            else:
                messages.error(request,"Enter your address to continue")
                return redirect('confirm_details',1)
        else:
            messages.error(request,"Only get request will be handled.")
    else:
        messages.error(request,"Login to continue")
        return redirect('login')
    
def log_out(request):
    auth.logout(request)
    return redirect('index')





