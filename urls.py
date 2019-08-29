from django.urls import path

from . import views
from .views import SearchResultsView

app_name = 'ppl_order_tracking'

urlpatterns = [
    path('', views.index, name='index'),
    path('search_results/', SearchResultsView.as_view(), name='search_results'),
    path('<str:po_number>/', views.detail, name='detail'),
]
