from django.db import models
from django.contrib.auth.models import User

class RoomType(models.Model):
    type_name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    base_price = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.type_name


class Room(models.Model):
    room_number = models.CharField(max_length=10)
    floor = models.IntegerField()
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)

    def __str__(self):
        return f"Room {self.room_number}"


class RoomPhoto(models.Model):
    room = models.ForeignKey(
        Room,
        related_name="photos",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="rooms/", null=True, blank=True)
    
from django.contrib.auth.models import User

class GuestProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


class Booking(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"Booking {self.id}"


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.id}"


class Registration(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    checkin_time = models.DateTimeField()
    checkout_time = models.DateTimeField(null=True, blank=True)
    checked_in_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admin_checked')

    def __str__(self):
        return f"Registration for Booking {self.booking.id}"

