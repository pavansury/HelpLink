from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import HelpRequest, Notification, UserProfile
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
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "login.html")


# -------------------- LOGOUT --------------------
def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


# -------------------- PROFILE PAGE --------------------
@login_required
def profile_view(request, username):
    # Get the user whose profile is being viewed
    user_obj = get_object_or_404(User, username=username)

    # Ensure profile exists (auto-create if missing)
    profile, created = UserProfile.objects.get_or_create(
        user=user_obj,
        defaults={"joined_date": timezone.now()},
    )

    # Stats section
    stats = [
        ("Total Helps", profile.total_helps or 0, "text-rose-500", "❤️"),
        ("Reputation", profile.reputation_points or 0, "text-orange-500", "🔥"),
        ("Requests Posted", user_obj.help_requests.count(), "text-purple-500", "📢"),
        ("Member Since", profile.joined_date.strftime("%b %Y"), "text-green-500", "📅"),
    ]

    # Category progress section
    category_progress = []
    category_qs = user_obj.help_requests.values('category').distinct()
    for c in category_qs:
        cat_name = c['category'] or 'General'
        count = user_obj.help_requests.filter(category=cat_name).count()
        category_progress.append({
            'category': cat_name,
            'count': count,
            'progress': min(100, count * 10),
            'color': 'from-blue-500 to-cyan-500',
            'icon': '💪'
        })

    # Recent activity section
    recent_activity = [
        {
            'action': hr.title,
            'person': hr.user.username,
            'category': hr.category or 'General',
            'time': hr.date_created.strftime('%b %d %Y')
        }
        for hr in user_obj.help_requests.order_by('-date_created')[:5]
    ]

    # Achievements section
    achievements = [
        {"name": "First Helper", "description": "Completed your first request", "icon": "🎉", "unlocked": True},
        {"name": "Community Star", "description": "Helped 10 different people", "icon": "⭐", "unlocked": True},
        {"name": "Consistent Helper", "description": "Helped someone 7 days in a row", "icon": "🔥", "unlocked": False},
    ]

    return render(request, 'profile.html', {
        "profile_user": user_obj,
        "profile": profile,
        "stats": stats,
        "category_progress": category_progress,
        "recent_activity": recent_activity,
        "achievements": achievements,
    })


# -------------------- MY PROFILE REDIRECT --------------------
@login_required
def my_profile_redirect(request):
    """When user clicks 'Profile', go to their own profile page instead of notifications."""
    return redirect('profile', username=request.user.username)


# -------------------- REQUESTS LIST --------------------
@login_required
def requests_list(request):
    categories = [
        'All', 'Loneliness', 'Stress Handling', 'Communication', 'Weight Lifting',
        'Ride Sharing', 'Electrical', 'Cleaning', 'Pet Care', 'Tutoring', 'Shopping', 'Moving'
    ]

    selected_category = request.GET.get('category')

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


# -------------------- HELP OFFER VIEW --------------------
@login_required
def help_view(request, request_id):
    help_request = get_object_or_404(HelpRequest, id=request_id)

    if request.method == 'POST':
        message = request.POST.get('message', '')

        # Create a notification for the requester
        Notification.objects.create(
            recipient=help_request.user,
            sender=request.user,
            help_request=help_request,
            message=message or f"{request.user.username} offered help on your request '{help_request.title}'!"
        )

        messages.success(request, "Help offer sent successfully!")
        return redirect('requests')

    return render(request, 'help.html', {'help_request': help_request})


# -------------------- NOTIFICATIONS VIEW --------------------
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})


# -------------------- ACCEPT REQUEST --------------------
@login_required
def accept_request(request, id):
    help_request = get_object_or_404(HelpRequest, id=id)
    help_request.is_accepted = True
    help_request.save()
    return redirect('notifications')


# -------------------- COMPLETE REQUEST --------------------
@login_required
def complete_request(request, id):
    help_request = get_object_or_404(HelpRequest, id=id)
    help_request.is_completed = True
    help_request.save()
    return redirect('notifications')


# -------------------- REQUEST DETAIL --------------------
def request_detail(request, request_id):
    help_request = get_object_or_404(HelpRequest, id=request_id)
    return render(request, "request_detail.html", {"help_request": help_request})
