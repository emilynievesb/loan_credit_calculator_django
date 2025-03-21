from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile 

class CustomUserAdmin(UserAdmin):
    model = UserProfile
    list_display = ('email', 'username', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(UserProfile, CustomUserAdmin)
