from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, HelpRequest,Notification


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'location', 'is_top_helper', 'total_helps', 'reputation_points')
    search_fields = ('full_name', 'user__username', 'location')


@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'category', 'urgency', 'status', 'created_at', 'is_accepted', 'is_completed')
    search_fields = ('title', 'user__username', 'category')
    list_filter = ('urgency', 'category', 'status')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'message', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'sender__username', 'message')
    list_filter = ('is_read',)
        
# ✅ Extend the default User admin to show related UserProfile inline
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Unregister the original User admin and register the extended one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
