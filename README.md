# SkyBooker ✈️  

SkyBooker is a web-based flight booking application built with Django. It allows users to search flights, book tickets, manage bookings, and includes an admin interface to manage flights and users.

---

## ✅ Features

- Home page / landing page  
- User registration and login  
- Flight search by source, destination, date, etc.  
- Flight listing and details  
- Booking of flights by passengers  
- Passenger details collection and booking confirmation  
- Display of booking history for users  
- Payment page & booking success confirmation (if implemented)  
- Admin dashboard / admin home for managing flights (for airlines/admins)  
- Contact us, profile pages, static pages like about/contact  

---

## 🚀 How to Run Locally

1. Clone the repository  
   ```bash
   git clone https://github.com/sanjaydevscripts/SkyBooker.git
   cd SkyBooker
   ```

2. Install dependencies (Django, Pillow, etc.)  
   ```bash
   pip install django pillow
   ```

3. Apply database migrations  
   ```bash
   python manage.py migrate
   ```

4. (Optional) Create a superuser for admin access  
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server  
   ```bash
   python manage.py runserver
   ```

6. Open your browser and go to  
   ```
   http://127.0.0.1:8000/
   ```

---

## 📝 Usage & Workflow

- New users can register and login.  
- Users can search for flights by specifying source, destination, date, and other details.  
- Flights matching the search criteria are listed.  
- Users can select a flight, enter passenger details, and book tickets.  
- Booking history is available for logged-in users.  
- Admins (or airlines) can log in via the admin dashboard to add/edit flights.  
- Static pages like contact, about, etc. are available via templates.  

---

> Developed by sanjaydevscripts — Feel free to reuse or extend as needed.
