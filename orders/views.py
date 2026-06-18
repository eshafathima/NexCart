from django.shortcuts import render,redirect
from .models import Order,orderedItem
from products.models import Product
from customer.models import Customer
# Create your views here.
def show_cart(request):
    user = request.user
    customer = request.user.customer_profile
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

def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        customer = user.customer_profile
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