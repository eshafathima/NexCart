from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Customer
# Create your views here.# Create your views here.
def show_account(request):
    if request.POST and 'register' in request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        #create user account
        user=User.objects.create(
             username=username,
             password=password,
             email=email
        )
        customer_obj = Customer.objects.create(  user=user,
             phone=phone,address=address)
    return render(request,'account.html')