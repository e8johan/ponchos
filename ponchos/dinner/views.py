from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

import json
import qrcode
import qrcode.image.svg
import socket

from .models import Order, Dish, OrderItem

_myip = ''

def _find_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    return s.getsockname()[0]

def url_qrcode(request):
    global _myip
    if _myip == '':
        _myip = _find_my_ip()
    img = qrcode.make("http://" + _myip + ":8000/", image_factory=qrcode.image.svg.SvgImage)
    res = HttpResponse(img.to_string(encoding='unicode'))
    res['Content-Type'] = 'image/svg+xml'
    return res


def index(request):
    issued_orders = Order.objects.filter(state=Order.State.ISSUED).order_by('order_time')
    completed_orders = Order.objects.filter(state=Order.State.COMPLETED).order_by('order_time')
    return render(request, 'dinner/index.html', { 'completed_orders': completed_orders, 'issued_orders': issued_orders })

def kitchen(request):
    orders = Order.objects.filter(state=Order.State.ISSUED).order_by('order_time')
    return render(request, 'dinner/kitchen.html', { 'orders': orders })

def place_order(request):
    dishes = Dish.objects.filter(is_available=True).order_by('dish_name')
    return render(request, 'dinner/place_order.html', { 'dishes': dishes })

def view_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'dinner/view_order.html', { 'order': order })

def api_place_order(request):
    if not request.method == 'POST':
        return  HttpResponseNotAllowed(["POST"])

    order = json.loads(request.body)

    dbOrder = Order(state = Order.State.ISSUED, orderer=order['orderer'], order_time = timezone.now())
    dbOrder.save()

    for dishId in order['dishes']:
        print(dishId)
        oi = OrderItem(order=dbOrder, dish=Dish.objects.get(pk=dishId[5:]), amount=order['dishes'][dishId])
        oi.save()

    return HttpResponse()

def api_cancel_order(request):
    if not request.method == 'POST':
        return  HttpResponseNotAllowed(["POST"])

    order = json.loads(request.body)
    dbOrder = get_object_or_404(Order, pk=order['order'])
    dbOrder.state = Order.State.CANCELLED
    dbOrder.save()

    return HttpResponse()

def api_complete_order(request):
    if not request.method == 'POST':
        return  HttpResponseNotAllowed(["POST"])

    order = json.loads(request.body)
    dbOrder = get_object_or_404(Order, pk=order['order'])
    dbOrder.state = Order.State.COMPLETED
    dbOrder.save()

    return HttpResponse()

def api_accept_order(request):
    if not request.method == 'POST':
        return  HttpResponseNotAllowed(["POST"])

    order = json.loads(request.body)
    dbOrder = get_object_or_404(Order, pk=order['order'])
    dbOrder.state = Order.State.CLOSED
    dbOrder.save()

    return HttpResponse()

