"""
URL configuration for SkyBooker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from flight import views

from flight.views import BookFlightView, PassengerDetailsView,PaymentSuccessView,download_ticket_pdf,BookingHistoryView,DeleteBookingView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home.as_view(),name='home'),
    path('register/',views.UserRegistration.as_view(),name='register'),
    path('login/',views.UserLogin.as_view(),name='login'),
    path('logout/',views.UserLogout.as_view(),name='logout'),
    path('contact/',views.CustomerSupportView.as_view(),name='contact'),
    path('for_airlines/',views.ForAirlines.as_view(),name='for_airlines'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('flight_details/',views.FlightSearchView.as_view(),name='flight_details'),
    path('book_flight/<int:flight_id>/', BookFlightView.as_view(), name='book_flight'),
    path('passenger_details/<int:booking_id>/', PassengerDetailsView.as_view(), name='passenger_details'),
    path('payment_success/<int:booking_id>/', PaymentSuccessView.as_view(), name='payment_success'),
    path('download_ticket/<int:booking_id>/', download_ticket_pdf, name='download_ticket'),
    path('booking_history/', BookingHistoryView.as_view(), name='booking_history'),
    path('delete_booking/<int:booking_id>/', DeleteBookingView.as_view(), name='delete_booking'),
    path('admin_home/', views.AdminHomeView.as_view(), name='admin_home'),
    path('dashboard/', views.DashBoardView.as_view(), name='dashboard'),
    path('delete_flight/<int:flight_id>/', views.DeleteFlightView.as_view(), name='delete_flight'),
    path('add_flight/', views.AddFlightView.as_view(), name='add_flight'),



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
