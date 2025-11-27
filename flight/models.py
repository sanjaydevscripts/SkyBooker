from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    passport_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username



class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    airline_name = models.CharField(max_length=50)
    from_city = models.CharField(max_length=50)
    to_city = models.CharField(max_length=50)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seats_available = models.PositiveIntegerField()
    TRAVEL_CLASS_CHOICES = [
        ('Economy', 'Economy'),
        ('Premium Economy', 'Premium Economy'),
        ('Business', 'Business'),
        ('First Class', 'First Class'),
    ]
    travel_class = models.CharField(max_length=20, choices=TRAVEL_CLASS_CHOICES, default='Economy')

    def __str__(self):
        return self.flight_number + " - " + self.from_city + " to " + self.to_city


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    total_passengers = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)


    def __str__(self):
        return self.user.username + " booked " + self.flight.flight_number + " - " + self.flight.from_city + " to " + self.flight.to_city


class Passenger(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
    full_name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=20)
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.full_name + self.passport_number

#
# COUNTRIES = [
#     ("Australia", "Australia"),
#     ("Japan", "Japan"),
#     ("United States", "United States"),
#     ("Brazil", "Brazil"),
#     ("China", "China"),
#     ("Israel", "Israel"),
#     ("Philippines", "Philippines"),
#     ("Malaysia", "Malaysia"),
#     ("Canada", "Canada"),
#     ("Chile", "Chile"),
#     ("Zimbabwe", "Zimbabwe"),
# ]

#
# class AddFlight(models.Model):
#     flight_number = models.CharField(max_length=50)
#     airline_name = models.CharField(max_length=100)
#
#     from_city = models.CharField(max_length=50, choices=COUNTRIES)
#     to_city = models.CharField(max_length=50, choices=COUNTRIES)
#
#     departure_date = models.DateField()
#     arrival_date = models.DateField()
#     departure_time = models.TimeField()
#     arrival_time = models.TimeField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     seats_available = models.IntegerField()
#     travel_class = models.CharField(max_length=20)


