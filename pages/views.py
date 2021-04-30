from django.shortcuts import render
from .models import *
import os, sys
sys.path.insert(1, os.getcwd()) 
from ThumkiStores.models import *

# Create your views here.

def block_printing(request):
    mydata = General_info.objects.first()
    categories = Category.objects.all()
    
    pg = request.GET.get('pg',1)
    
    info = Block_printing.objects.filter(page_number=pg).first()
    
    return render(request,'pages/block_printing.html', { 'title':'Block printing' ,'mydata': mydata,'categories':categories,'info':info })
