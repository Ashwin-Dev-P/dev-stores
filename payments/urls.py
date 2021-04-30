from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('payment_success',views.payment_success,name='payment_success'),
    path('payment_paytm', views.payment_paytm,name='payment_paytm'),
    path('response/<int:id>', views.response),
    path('paypal_recieve',views.paypal_recieve,name='paypal_recieve'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)