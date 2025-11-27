from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models.fields import return_None
from django.shortcuts import render,redirect
from django.views import View
import razorpay

from flight.forms import SignUpForm,LoginForm,ContactUsForm,ProfileForm,UserUpdateForm,PassengerForm,BookingContactForm,FlightForm

from flight.models import Flight,Booking
from razorpay import Payment


class Home(View):
    def get(self,request):
        return render(request,'Home.html')

import re
def is_valid_passport(passport_number):
    """
    Simple example validation:
    - Must start with a letter
    - Followed by 7 digits
    """
    pattern = r'^[A-Z][0-9]{7}$'
    return re.match(pattern, passport_number) is not None


class UserRegistration(View):
    def get(self, request):
        user_form = SignUpForm()
        profile_form = ProfileForm()
        return render(request, 'Register.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form_instance = SignUpForm(request.POST)
        profile_form_instance = ProfileForm(request.POST)

        if user_form_instance.is_valid() and profile_form_instance.is_valid():
            passport_number = profile_form_instance.cleaned_data.get('passport_number')

            # Validate passport
            if not is_valid_passport(passport_number):
                messages.error(request, "Invalid passport number! Please enter a valid one.")
                return render(request, 'Register.html', {
                    'user_form': user_form_instance,
                    'profile_form': profile_form_instance
                })

            # Save User and Profile
            user = user_form_instance.save(commit=False)
            user.save()

            profile = profile_form_instance.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "Account created successfully!")
            return redirect('login')

        messages.error(request, "Please correct the errors below.")
        return render(request, 'Register.html', {
            'user_form': user_form_instance,
            'profile_form': profile_form_instance
        })



class UserLogin(View):
    def get(self,request):
        form_instance=LoginForm()
        return render(request,'login.html',{'form':form_instance})
    def post(self,request):
        form_instance = LoginForm(request.POST)
        if form_instance.is_valid():
            data = form_instance.cleaned_data
            name = data['username']
            pwd = data['password']
            user = authenticate(username=name, password=pwd)

            if user:
                login(request, user)


                # Redirect admin to admin dashboard
                if user.is_staff:
                    return redirect('admin_home')

                # Redirect normal user to home page
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
                return render(request, 'login.html', {'form': form_instance})


class UserLogout(View):
    def get(self,request):
        logout(request)
        return redirect('home')


class CustomerSupportView(View):
    def get(self,request):
        form_instance=ContactUsForm()
        return render(request, 'contact_us.html', {'form': form_instance})



class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect if not logged in

        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

        return render(request, 'profile.html', {'user_form': user_form,'profile_form': profile_form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, 'profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })



class ForAirlines(View):
    def get(self,request):
        return render(request,'forairlines.html')




class FlightSearchView(View):

    def post(self, request):
        from_city = request.POST.get('from_city')
        to_city = request.POST.get('to_city')
        departure_date = request.POST.get('departure_date')
        travel_class = request.POST.get('travel_class')

        flights = Flight.objects.filter(
            from_city__iexact=from_city,
            to_city__iexact=to_city,
            departure_date=departure_date,
            travel_class__iexact=travel_class,
        )
        return render(request, 'flight_results.html', {'flights': flights})


from django.http import Http404, HttpResponse


class BookFlightView(View):
    def get(self, request,flight_id):
        try:
            flight = Flight.objects.get(id=flight_id)
        except Flight.DoesNotExist:
            raise Http404("Flight not found")

        if flight.seats_available == 0:
            messages.error(request, "Sorry, no seats available for this flight.")
            return render(request, 'book_flight.html', {'flight': flight, 'no_seats': True})

        return render(request, 'book_flight.html', {'flight': flight, 'no_seats': False})

    def post(self, request, flight_id):
        # 1. Get flight
        try:
            flight = Flight.objects.get(id=flight_id)
        except Flight.DoesNotExist:
            messages.error(request, "Flight not found!")
            return redirect('home')

        # 2. Get passenger count from form
        passenger_count = int(request.POST.get('passenger_count', 1))

        if passenger_count > flight.seats_available:
            messages.error(
                request,
                messages.error(request,"Only " + str(flight.seats_available) + " seats are available! Please reduce the number of passengers."))
            return render(request, 'book_flight.html', {'flight': flight, 'no_seats': False})

        # 3. Create a booking record now
        booking = Booking.objects.create(
            user=request.user,
            flight=flight,
            total_passengers=passenger_count,
            total_price=flight.price * passenger_count,  # optional, can update later
            contact_email="",  # will fill later
            contact_phone=""  # will fill later
        )

        # 4. Redirect to passenger details page using booking.id
        return redirect('passenger_details', booking_id=booking.id)






class PassengerDetailsView(View):
    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return HttpResponse("Booking not found.", status=404)

        flight = booking.flight
        passenger_count = booking.total_passengers


        passenger_forms = [PassengerForm(prefix=str(i)) for i in range(passenger_count)]
        contact_form = BookingContactForm()

        return render(request, 'passenger_details.html', {
            'flight': flight,
            'passenger_forms': passenger_forms,
            'contact_form': contact_form,
            'total_price': booking.total_price,
            'total_passengers': passenger_count,
            'booking_id': booking.id
        })

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return HttpResponse("Booking not found.", status=404)

        passenger_count = booking.total_passengers
        passenger_forms = [PassengerForm(request.POST, prefix=str(i)) for i in range(passenger_count)]

        all_valid = True
        for form in passenger_forms:
            if form.is_valid():
                passport_number = form.cleaned_data.get('passport_number')
                if not is_valid_passport(passport_number):
                    form.add_error('passport_number',
                                   "Invalid passport number! Must be 1 capital letter followed by 7 digits.")
                    all_valid = False
            else:
                all_valid = False

        if all_valid:

            for form in passenger_forms:
                passenger = form.save(commit=False)
                passenger.booking = booking
                passenger.save()

            # Create Razorpay order
            client = razorpay.Client(auth=('rzp_test_RJOTa18jmnSyYc', 'jC1EgRTw7Na85oUrC2yvNESQ'))
            response_payment = client.order.create(dict(amount=int(booking.total_price * 100), currency='INR'))

            return render(request, 'payment.html', {
                'payment': response_payment,
                'booking': booking
            })

        # Re-render page with validation errors
        return render(request, 'passenger_details.html', {
            'flight': booking.flight,
            'passenger_forms': passenger_forms,
            'total_price': booking.total_price,
            'total_passengers': booking.total_passengers,
            'booking_id': booking.id
        })


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class PaymentSuccessView(View):
    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
            flight = booking.flight
        except Booking.DoesNotExist:
            return HttpResponse("Booking not found.", status=404)

        # Reduce available seats
        if flight.seats_available >= booking.total_passengers:
            flight.seats_available -= booking.total_passengers
            flight.save()

        # Show success (ticket info)
        return render(request, 'payment_success.html', {
            'booking': booking,
            'flight': flight
        })


from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from .models import Booking

def download_ticket_pdf(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    flight = booking.flight
    passengers = booking.passengers.all()

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Ticket_{booking.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, height - 50, "Flight Ticket")

    # Flight details
    p.setFont("Helvetica", 12)
    y = height - 100
    p.drawString(100, y, f"Flight Number: {flight.flight_number}")
    y -= 20
    p.drawString(100, y, f"Airline: {flight.airline_name}")
    y -= 20
    p.drawString(100, y, f"From: {flight.from_city}  →  To: {flight.to_city}")
    y -= 20
    p.drawString(100, y, f"Departure: {flight.departure_date}")
    y -= 30

    # Booking details
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "Passenger Details:")
    y -= 20
    p.setFont("Helvetica", 12)

    for i, passenger in enumerate(passengers, start=1):
        p.drawString(120, y, f"{i}. {passenger.full_name} | Passport: {passenger.passport_number} | Age: {passenger.age}")
        y -= 20

    y -= 20
    p.drawString(100, y, f"Total Passengers: {booking.total_passengers}")
    y -= 20
    p.drawString(100, y, f"Total Paid: ₹{booking.total_price}")

    # Footer
    y -= 40
    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(width / 2, y, "Thank you for booking with SkyBooker ✈")

    p.showPage()
    p.save()

    return response




class BookingHistoryView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        # Get all bookings for the logged user
        bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')

        return render(request, 'booking_history.html', {'bookings': bookings})

class DeleteBookingView(View):
    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            raise Http404("Booking not found")
        booking.delete()
        messages.success(request, "Booking deleted successfully!")
        return redirect('booking_history')

class AdminHomeView(View):
    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('login')

        return render(request, 'admin_home.html')

class DashBoardView(View):
    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('login')

        flights = Flight.objects.all().order_by('-departure_date')
        return render(request, 'admin_dashboard.html', {'flights': flights})


class DeleteFlightView(View):
    def post(self, request, flight_id):
        if not request.user.is_staff:
            return HttpResponse("Unauthorized", status=403)

        try:
            flight = Flight.objects.get(id=flight_id)
            flight.delete()
            messages.success(request, "Flight deleted successfully!")
        except Flight.DoesNotExist:
            messages.error(request, "Flight not found!")

        return redirect('admin_home')



class AddFlightView(View):
    def get(self, request):
        if not request.user.is_staff:
            return redirect('login')

        form = FlightForm()
        return render(request, 'add_flight.html', {'form': form})

    def post(self, request):
        if not request.user.is_staff:
            return redirect('login')

        form = FlightForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Flight added successfully!")
            return redirect('admin_home')

        messages.error(request, "Please correct the errors below.")
        return render(request, 'add_flight.html', {'form': form})









