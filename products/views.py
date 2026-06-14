from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.
def index(request):
    return render(request,'index.html')

def list_product(request):
    """returns product list page"""
    return render(request,'products.html')

def details_product(request):
    return render(request,'product_detail.html')
