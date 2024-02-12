from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('kitchen/', views.kitchen, name='kitchen'),
    path('orders/new/', views.place_order, name='place_order'),
    path('orders/<int:order_id>/', views.view_order, name='view_order'),
    path('qr/', views.url_qrcode, name='qrcode'),

    path('api/place_order', views.api_place_order, name='api_place_order'),
    path('api/cancel_order', views.api_cancel_order, name='api_cancel_order'),
    path('api/complete_order', views.api_complete_order, name='api_complete_order'),
    path('api/accept_order', views.api_accept_order, name='api_accept_order'),
]
