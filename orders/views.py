
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, orderedItem
from products.models import Product
from customer.models import Customer
from django.contrib import messages


def get_customer_profile(user):
    if not user.is_authenticated:
        return None
    customer, created = Customer.objects.get_or_create(
        user=user,
        defaults={
            'address': '',
            'phone': 0,
        }
    )
    return customer


@login_required(login_url='home')
def show_cart(request):
    customer = get_customer_profile(request.user)
    cart_obj, created = Order.objects.get_or_create(
        owner=customer,
        order_status=Order.CART_STAGE
    )

    cart_items = cart_obj.added_items.select_related('product').all()
    subtotal = sum(item.subtotal for item in cart_items)
    tax = round(subtotal * 0.15, 2) if subtotal else 0
    total = subtotal + tax

    context = {
        'cart': cart_obj,
        'cart_items': cart_items,
        'cart_subtotal': subtotal,
        'cart_tax': tax,
        'cart_total': total,
    }
    return render(request, 'cart.html', context)

@login_required(login_url='account')

def show_orders(request):
    user=request.user
    customer = get_customer_profile(request.user)
    all_orders=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context={'orders':all_orders}
    return render(request, 'orders.html', context)


@login_required(login_url='account')
def view_orders(request):
    user=request.user
    customer = get_customer_profile(request.user)
   

   
    
    return render(request, 'cart.html', context)



@login_required(login_url='home')
def checkout(request):
    try:
        if request.method == 'POST':
            customer = get_customer_profile(request.user)
            cart_total = float(request.POST.get('total') or 0)
            order_obj = Order.objects.get(owner=customer, order_status=Order.CART_STAGE)

            if order_obj:
                order_obj.order_status = Order.ORDER_CONFIRMED
                order_obj.save()
                messages.success(request, "Your order is confirmed. Your item will be delivered in 2 days.")
        else:
            messages.error(request, "No item in cart.")
    except Order.DoesNotExist:
        messages.error(request, "No item in cart.")
    except Exception:
        messages.error(request, "Something went wrong. Please try again.")
    return redirect('cart')


@login_required(login_url='home')
def add_to_cart(request):
    if request.method == 'POST':
        customer = get_customer_profile(request.user)
        product_id = request.POST.get('product_id')
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except (TypeError, ValueError):
            quantity = 1

        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return redirect('cart')

        ordered_item, item_created = orderedItem.objects.get_or_create(
            product=product,
            owner=cart_obj,
            defaults={'quantity': quantity}
        )

        if not item_created:
            ordered_item.quantity += quantity
            ordered_item.save()

    return redirect('cart')


@login_required(login_url='home')
def removefromcart(request, pk):
    try:
        item = orderedItem.objects.get(pk=pk)
        item.delete()
    except orderedItem.DoesNotExist:
        pass
    return redirect('cart')

