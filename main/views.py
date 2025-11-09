from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse

from .models import HelpRequest, UserProfile
from .forms import SignupForm, LoginForm, HelpRequestForm


# -------------------- HOME PAGE --------------------
def index(request):
    quick_stats = [
        {"key": "contrib", "label": "Your Contributions", "value": "47", "color": "text-rose-500"},
        {"key": "people", "label": "People Helped", "value": "35", "color": "text-blue-500"},
        {"key": "chats", "label": "Active Chats", "value": "3", "color": "text-purple-500"},
        {"key": "month", "label": "This Month", "value": "+12", "color": "text-green-500"},
    ]

    latest_requests = HelpRequest.objects.order_by('-date_created')[:6]

    context = {
        "quick_stats": quick_stats,
        "recent_requests": latest_requests,
    }
    return render(request, "index.html", context)


# -------------------- SIGNUP --------------------
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


# -------------------- LOGIN --------------------
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")  # Redirect to homepage
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")

# -------------------- LOGOUT --------------------
def Logout(request):
    auth_logout(request)
    return redirect('home')


# -------------------- PROFILE --------------------
@login_required
def profile_view(request):
    user = request.user
    profile = getattr(user, 'profile', None)

    stats = [
        ("Requests", user.help_requests.count(), "text-rose-500", "❤️"),
        ("Completed", user.help_requests.filter(status='Completed').count(), "text-green-500", "✅"),
        ("Pending", user.help_requests.filter(status='Pending').count(), "text-yellow-500", "⌛"),
        ("Accepted", user.help_requests.filter(status='Accepted').count(), "text-indigo-500", "⭐"),
    ]

    # category progress
    category_progress = []
    category_qs = user.help_requests.values('category').distinct()
    for c in category_qs:
        cat_name = c['category'] or 'General'
        count = user.help_requests.filter(category=cat_name).count()
        category_progress.append({
            'category': cat_name,
            'count': count,
            'progress': min(100, count * 10),
            'color': 'from-blue-500 to-cyan-500',
            'icon': '💪'
        })

    # recent activity
    recent_activity = [
        {'action': hr.title, 'person': hr.user.username, 'category': hr.category or 'General',
         'time': hr.date_created.strftime('%b %d %Y')}
        for hr in user.help_requests.order_by('-date_created')[:5]
    ]

    achievements = [
        {"name": "First Helper", "description": "Completed your first request", "icon": "🎉", "unlocked": True},
        {"name": "Community Star", "description": "Helped 10 different people", "icon": "⭐", "unlocked": True},
        {"name": "Consistent Helper", "description": "Helped someone 7 days in a row", "icon": "🔥", "unlocked": False},
    ]

    return render(request, 'profile.html', {
        "profile": profile,
        "stats": stats,
        "category_progress": category_progress,
        "recent_activity": recent_activity,
        "achievements": achievements,
    })


# -------------------- REQUESTS LIST --------------------
@login_required
def requests_list(request):
    categories = [
        'All', 'Loneliness', 'Stress Handling', 'Communication', 'Weight Lifting',
        'Ride Sharing', 'Electrical', 'Cleaning', 'Pet Care', 'Tutoring', 'Shopping', 'Moving'
    ]

    selected_category = request.GET.get('category')

    # Filter by category
    if selected_category and selected_category != 'All':
        requests_qs = HelpRequest.objects.filter(category=selected_category)
    else:
        requests_qs = HelpRequest.objects.all()

    context = {
        'requests': requests_qs.order_by('-date_created'),
        'categories': categories,
        'selected_category': selected_category,
    }

    return render(request, 'requests.html', context)


# -------------------- ADD REQUEST --------------------
@login_required
def add_request(request):
    if request.method == 'POST':
        form = HelpRequestForm(request.POST)
        if form.is_valid():
            help_request = form.save(commit=False)
            help_request.user = request.user
            help_request.save()
            messages.success(request, "Request added successfully!")
            return redirect('requests')
    else:
        form = HelpRequestForm()

    return render(request, 'requests/section2.html', {'form': form})


# -------------------- SETTINGS PAGE --------------------
def settings_page(request):
    return render(request, 'settings.html')
