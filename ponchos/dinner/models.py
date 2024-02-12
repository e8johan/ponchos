from django.db import models

class Dish(models.Model):
    dish_name = models.CharField(max_length=200)
    is_available = models.BooleanField()

class Order(models.Model):
    class State(models.IntegerChoices):
        OPEN = 1        # Order is being edited
        ISSUED = 2      # Order has been issued for the kitchen
        COMPLETED = 3   # Order has been completed by the kitchen
        CLOSED = 4      # Order has been closed (and picked up)
        CANCELLED = 5   # Order has been cancelled

    state = models.IntegerField(choices=State)
    orderer = models.CharField(max_length=100)
    preparer = models.CharField(max_length=100, null=True)
    order_time = models.DateTimeField()
    complete_time = models.DateTimeField(null=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    amount = models.IntegerField()
