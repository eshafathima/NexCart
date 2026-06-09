from django.db import models

# Create your models here.
class Order(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,'Live'),(DELETE,'Delete'))
    CART_STAGE=0
    ORDER_CONFIRMED=1
    ORDER_PROCESSED=2
    ORDER_DELIVERED=3
    ORDER_REJECTED=4
    STATUS_CHOICE=((CART_STAGE,"CART_STAGE"), (ORDER_PROCESSED,"ORDER_PROCESSED"), (ORDER_DELIVERED,"ORDER_DELIVERED"), (ORDER_REJECTED,"ORDER_REJECTED"))
    order_status=models.IntegerField(choices=STATUS_CHOICE,default=CART_STAGE)
    owner=models.ForeignKey('customer.Customer', on_delete=models.SET_NULL, null=True, related_name='cart_owner')
    delete_status=models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)

class orderedItem(models.Model):
    product=models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, related_name='added_cart')
    quantity=models.IntegerField(default=1)
    owner=models.ForeignKey('orders.order', on_delete=models.CASCADE, related_name='added_items')