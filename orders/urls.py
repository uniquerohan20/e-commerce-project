from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/<str:order_id>/', views.order_success, name='order_success'),
    path('order-history/', views.order_history, name='order_history'),
    path('order/<str:order_id>/', views.order_detail, name='order_detail'),
    path('cancel-order/<str:order_id>/', views.cancel_order, name='cancel_order'),
]
