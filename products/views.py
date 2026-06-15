from django.shortcuts import render, get_object_or_404
from .models import Product
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    featured_product=Product.objects.order_by('priority')[:2]
    latest_product=Product.objects.order_by('-priority')[:3]
    context={'featured' :featured_product,
             'latest':latest_product }
    return render(request,'index.html',context)

def list_product(request):
    """returns product list page"""
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    product_list=Product.objects.order_by('priority')
    product_paginator=Paginator(product_list,2)
    product_list=product_paginator.get_page(page )
    context={'Products':product_list}
    return render(request,'products.html',context)
   
def details_product(request,pk):
    product=Product.objects.get(pk=pk)
    context={'product':product}
    return render(request,'product_detail.html',context)
