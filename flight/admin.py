from django.contrib import admin

from flight.models import Profile,Flight,Booking,Passenger

admin.site.register(Profile)
admin.site.register(Flight)
admin.site.register(Booking)
admin.site.register(Passenger)
