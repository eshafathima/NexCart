from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth import authenticate,login,logout
from  django.contrib import messages 
# Create your views here.# Create your views here.
def signout(request):
    logout(request)
    return redirect('home')
def show_account(request):
    context={}
    if request.POST and 'register' in request.POST:
        context['register']=True
    if request.POST and 'login' in request.POST:
        context['register']=False
        try:
            username=request.POST.get('username')
            password=request.POST.get('password')
            email=request.POST.get('email')
            address=request.POST.get('address')
            phone=request.POST.get('phone')
            #create user account
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            customer_obj = Customer.objects.create(
                user=user,
                phone=phone,
                address=address
            )
            messages.success(request, "Account Creation Successfull")
            return redirect('home')
        except Exception as e:
            messages.error(request,"Duplicate username or invalid credential")
    if request.POST and request.POST.get('action') == 'login':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate( request,username=username,password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'invalid credential')
    return render(request,'account.html',context)
def home(request):
    return render(request,'index.html')