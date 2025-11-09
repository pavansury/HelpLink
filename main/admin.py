# main/admin.py
from django.contrib import admin
from .models import UserProfile, HelpRequest

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'location')

@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'date_created')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description', 'user__username')
