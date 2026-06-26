from django.contrib import admin
from orders.models import Order, orderedItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'order_status', 'total_price', 'created_at')
    readonly_fields = ('total_price',)

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total Price'


admin.site.register(Order, OrderAdmin)
admin.site.register(orderedItem)
