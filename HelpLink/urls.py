from django.contrib import admin
from django.urls import path,include
from main import views  # replace 'main' with your app name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # ✅ This includes app URLs
    path('', views.index, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('requests/', views.requests_list, name='requests'),
    path('requests/add/', views.add_request, name='add_request'),
    path('settings/', views.settings_page, name='settings'),
]
