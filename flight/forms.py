from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from flight.models import Profile,Passenger,Flight



class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))



class ContactUsForm(forms.Form):
    email=forms.CharField()
    subject=forms.CharField(max_length=40)
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Your Message',
            'class': 'form-control',
            'rows': 5  # Number of visible rows
        })
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=['phone_number','address','passport_number']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['full_name', 'passport_number', 'age']



class BookingContactForm(forms.Form):
    phone_number = forms.CharField(label="Phone Number", max_length=15)
    email = forms.EmailField(label="Email")

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = "__all__"
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
            'departure_time': forms.TimeInput(attrs={'type': 'time'}),
            'arrival_time': forms.TimeInput(attrs={'type': 'time'}),
        }


