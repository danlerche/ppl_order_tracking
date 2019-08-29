from django.shortcuts import render, get_object_or_404
from django.db.models import Q # for search
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import PurchaseOrder, ItemsArrived, Vender
from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
import datetime
import calendar

def index(request):
    items = ItemsArrived.objects.all()
    purchase_order = PurchaseOrder.objects.all()
    items_received_per_po = ItemsArrived.objects.values('po_number_id').annotate(sum_items=Sum('items_received'))
    vender = Vender.objects.all()
    list_po = ItemsArrived.objects.values_list('po_number')
    list_pos = PurchaseOrder.objects.values_list('po_number')
    total_items_ordered = PurchaseOrder.objects.aggregate(Sum('items_ordered'))
    total_items_received = ItemsArrived.objects.filter(po_number__in=list_po).aggregate(Sum('items_received'))
    now = datetime.datetime.now()
    today = datetime.date.today()
    sub_one_day = today.replace(day=1)
    previous_month_sub = sub_one_day - datetime.timedelta(days=1)
    previous_month = previous_month_sub.month
    previous_month_name = calendar.month_name[previous_month]
    current_month = now.month
    current_month_items = ItemsArrived.objects.filter(date_received__month=current_month).aggregate(sum_month=Sum('items_received'))
    previous_month_items = ItemsArrived.objects.filter(date_received__month=previous_month).aggregate(sum_month=Sum('items_received'))
    po_content_type = ContentType.objects.get(model='purchaseorder')
    logs = LogEntry.objects.filter(content_type_id=po_content_type, action_flag=1)
    user = User.objects.all()

    return render(request, 'ppl_order_tracking/tracking.html', {
        'purchase_order': purchase_order,
        'items': items,
        'items_received_per_po': items_received_per_po,
        'total_items_received': total_items_received,
        'total_items_ordered': total_items_ordered,
        'now': now,
        'current_month_items': current_month_items,
        'previous_month_name': previous_month_name,
        'previous_month_items': previous_month_items,
        'user': user,
        'logs': logs,
})

def detail(request, po_number):
    po_details = get_object_or_404(PurchaseOrder, pk=po_number)
    po_info = ItemsArrived.objects.filter(po_number_id=po_number)
    sum_po = ItemsArrived.objects.all()

    return render(request, 'ppl_order_tracking/detail.html', {
    'po_details': po_details,
    'po_info': po_info,
    'sum_po': sum_po,
})

class SearchResultsView(ListView):
    model = PurchaseOrder
    template_name = 'ppl_order_tracking/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = PurchaseOrder.objects.filter(
            Q(po_number__icontains=query) | Q(items_ordered__icontains=query) | Q(vender__vender_name__icontains=query)
        )
        return object_list
