# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),  # if login_view exists
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('requests/', views.requests_list, name='requests'),
    path('add-request/', views.add_request, name='addRequest'),
    #path('help/', views.help_view, name='help'),
    path('help/<int:request_id>/', views.help_view, name='help'),
    path('notifications/', views.notifications_view, name='notifications'),
]
