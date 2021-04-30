from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        
        path('',views.index,name='index'),
        path('index',views.index,name=''),
        path('shop',views.shop,name='shop'),
        path('view/<int:id>',views.view,name='view'),
        path('viewtest',views.viewtest,name="viewtest"), 
        path('contact_us',views.contact_us,name='contact_us'),
        path('FAQ_page',views.FAQ_page,name='FAQ_page'),
        path('Subscribe',views.Subscribe,name='Subscribe'),
        path('cart',views.cart,name='cart'),
        path('cart_remove',views.cart_remove,name='cart_remove'),
        path('cart_add_quantity',views.cart_add_quantity,name='cart_add_quantity'),
        path('cart_subtract_quantity',views.cart_subtract_quantity,name='cart_subtract_quantity'),
        path('reviews',views.reviews,name='reviews'),
        path('profile/<int:edit>',views.profile,name='profile'),
        path('payment_selection',views.payment_selection,name='payment_selection'),
        path('confirm_details/<int:edit>',views.confirm_details,name='confirm_details'),
        
       
        path('log_out',views.log_out,name='log_out'),
        
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)