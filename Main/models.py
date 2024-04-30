from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.user.username


class Item(models.Model):
    STATUS_CHOICES = (
        ("available", "Available"),
        ("sold", "Sold"),
    )
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to="item_pictures/")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )
    bought_by = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
    )
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=1000, default="")
