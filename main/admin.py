from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, HelpRequest


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'location')
    search_fields = ('user__username', 'full_name', 'location')
    list_filter = ('location',)


@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'urgency', 'date_created')
    list_filter = ('status', 'category', 'urgency')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-date_created',)


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
