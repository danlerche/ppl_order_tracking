from django.contrib import admin
from django.contrib.admin.models import LogEntry
from ppl_order_tracking.models import PurchaseOrder, ItemsArrived, Vender

class ItemsArrivedInline(admin.TabularInline):
    model = ItemsArrived
    extra = 1

@admin.register(PurchaseOrder)
class POAdmin(admin.ModelAdmin):
    inlines = [
        ItemsArrivedInline,

    ]

admin.site.register(Vender)
admin.site.register(LogEntry)
