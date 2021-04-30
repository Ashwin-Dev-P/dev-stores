from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.admins_login,name='admins_login'),
    path('admins_login',views.admins_login,name='admins_login'),
    path('orders/<int:delivered>',views.orders,name='orders'),
    path('orders_info/<str:payment_id>',views.orders_info,name='orders_info'),
    path('messages_recieved_func/<int:read>',views.messages_recieved_func,name='messages_recieved_func'),
    path('subscribed_customers',views.subscribed_customers,name='subscribed_customers'),
    path('admins_log_out',views.admins_log_out,name='admins_log_out'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)