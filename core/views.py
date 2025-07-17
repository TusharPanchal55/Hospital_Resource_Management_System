import bcrypt
import base64
import numpy as np

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .mongo import users_collection
from .mongo import usage_collection
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from .mongo import users_collection
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        role = request.POST.get('role')
        
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return redirect('signup')

        if users_collection.find_one({'username': username}):
            messages.error(request, 'Username already exists.')
            return redirect('signup')

        # Hash the password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # Store the base64-encoded version (safe for JSON/Mongo)
        hashed_pw_b64 = base64.b64encode(hashed_pw).decode('utf-8')

        users_collection.insert_one({
            'username': username,
            'password': hashed_pw_b64,
            'email': email,
            'full_name': full_name,
            'role': role
        })

        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')

    return render(request, 'signup.html')


def custom_login_view(request):
    if request.session.get('session_expired'):
        messages.warning(request, "Session expired due to inactivity. Please log in again.")
        del request.session['session_expired']

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_data = users_collection.find_one({
            'username': {'$regex': f'^{username.strip()}$', '$options': 'i'}
        })

        if user_data:

            hashed_pw_b64 = user_data['password']
            try:
                hashed_pw_bytes = base64.b64decode(hashed_pw_b64)
            except Exception as e:
                messages.error(request, "Something went wrong. Please contact admin.")
                return render(request, 'login.html')

            if bcrypt.checkpw(password.encode('utf-8'), hashed_pw_bytes):
                django_user, _ = User.objects.get_or_create(username=user_data['username'])
                login(request, django_user)

                request.session['full_name'] = user_data.get('full_name', 'User')
                request.session['email'] = user_data.get('email', '')
                request.session['role'] = user_data.get('role', 'guest')

                messages.success(request, "Login successful!", extra_tags='login_page')
                return redirect('dashboard')

        messages.error(request, "Invalid credentials", extra_tags='login_page')

    return render(request, 'login.html')


def home(request):
    return redirect('login')


@login_required
def dashboard_view(request):
    role = request.session.get('role', '')
    blocked_pages = ["login", "signup"]
    current_url_name = request.resolver_match.url_name
    request.show_navbar = (
        request.user.is_authenticated and current_url_name not in blocked_pages
    )

    # 🧠 AI Forecast Logic — Only run if Admin, Doctor, or Nurse
    forecast_data = []
    if role in ['Admin', 'Doctor', 'Nurse']:
        records = list(usage_collection.find().sort("date", 1))

        if len(records) >= 3:
            try:
                # Convert dates to X values
                dates = [datetime.strptime(r['date'], "%Y-%m-%d") for r in records]
                days = np.array([(d - dates[0]).days for d in dates]).reshape(-1, 1)
                icu_vals = np.array([r['icu_beds_used'] for r in records])
                oxy_vals = np.array([r['oxy_cylinders'] for r in records])

                # Train regression models
                icu_model = LinearRegression().fit(days, icu_vals)
                oxy_model = LinearRegression().fit(days, oxy_vals)

                # Predict next 3 days
                # Predict next 3 days
                last_day = days[-1][0]
                ppe_vals = np.array([r['ppe_kits'] for r in records])  # ⬅️ Add PPE
                ppe_model = LinearRegression().fit(days, ppe_vals)     # ⬅️ Train model

                for i in range(1, 4):
                    future_day = last_day + i
                    future_date = dates[-1] + timedelta(days=i)
                    predicted_icu = int(round(icu_model.predict([[future_day]])[0]))
                    predicted_oxy = int(round(oxy_model.predict([[future_day]])[0]))
                    predicted_ppe = int(round(ppe_model.predict([[future_day]])[0]))

                    forecast_data.append({
                    'date': future_date.strftime("%Y-%m-%d"),
                    'icu': max(predicted_icu, 0),
                    'oxygen': max(predicted_oxy, 0),
                    'ppe': max(predicted_ppe, 0),
                    })

            except Exception as e:
                print(f"⚠️ Forecasting error: {e}")
                forecast_data = []

    # 📦 Pack context with navbar and forecast
    context = {
        'show_navbar': request.show_navbar,
        'forecast': forecast_data,
    }

    # Render based on role
    if role == 'Admin':
        return render(request, 'dashboards/admin_dashboard.html', context)
    elif role == 'Doctor':
        return render(request, 'doctor/admin_dashboard.html', context)
    elif role == 'Nurse':
        return render(request, 'nurse/admin_dashboard.html', context)
    else:
        messages.error(request, "Unauthorized access.")
        return redirect('login')


    


@login_required
def add_view(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        icu = int(request.POST.get('icu_beds_used'))
        oxy = int(request.POST.get('oxy_cylinders'))
        ppe = int(request.POST.get('ppe_kits'))

        usage_collection.insert_one({
            'date': date,
            'ppe_kits': ppe,
            'icu_beds_used': icu,
            'oxy_cylinders': oxy,
            'added_by': request.user.username,
            'created_at': timezone.now()
        })

        messages.success(request, "Resource usage data added successfully.", extra_tags='add_page')
        return render(request, 'add_data.html')

    return render(request, 'add_data.html')

@login_required
def list_view(request):
    mongo_records = usage_collection.find().sort("date", -1)

    records = []
    for doc in mongo_records:
        records.append({
            "date": doc.get("date"),
            "ppe_kits": doc.get("ppe_kits", 0),
            "icu_beds_used": doc.get("icu_beds_used", 0),
            "oxy_cylinders": doc.get("oxy_cylinders", 0),
            "added_by": {"username": doc.get("added_by", "Unknown")}
        })

    return render(request, 'list.html', {'records': records})



