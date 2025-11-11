from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profile URLs
    path('profile/', views.my_profile_redirect, name='my_profile_redirect'),
    path('profile/<str:username>/', views.profile_view, name='profile'),

    path('requests/', views.requests_list, name='requests'),
    path('add-request/', views.add_request, name='addRequest'),
    path('help/<int:request_id>/', views.help_view, name='help'),
    path('request/<int:request_id>/', views.request_detail, name='request_detail'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('accept/<int:id>/', views.accept_request, name='accept_request'),
    path('complete/<int:id>/', views.complete_request, name='complete_request'),
]
