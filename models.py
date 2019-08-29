from django.db import models
from django.db.models import Func, F, Sum

class Vender(models.Model):
    vender_name = models.CharField(max_length=50)
    def __str__(self):
        return self.vender_name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=30, primary_key=True, editable=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    items_ordered = models.IntegerField(null=True, default=0, help_text="Enter 0 for all standing orders")
    vender = models.ForeignKey(Vender, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.po_number

class ItemsArrived(models.Model):
    date_received = models.DateField()
    items_received = models.IntegerField(default=0)
    po_number = models.ForeignKey(PurchaseOrder, related_name='purchases', on_delete=models.CASCADE, default=6)

    class Meta:
       verbose_name_plural = "Items Arrived"
