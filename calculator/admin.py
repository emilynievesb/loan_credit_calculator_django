from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, LoanCalculation

class CustomUserAdmin(UserAdmin):
    model = UserProfile
    list_display = ('email', 'username', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(UserProfile, CustomUserAdmin)


@admin.register(LoanCalculation)
class LoanCalculationAdmin(admin.ModelAdmin):
    list_display = ('user', 'calculation_type', 'calculation_subtype', 'resultado', 'created_at')
    list_filter = ('calculation_type', 'calculation_subtype', 'created_at')
    search_fields = ('user__username', 'calculation_type', 'calculation_subtype')
    readonly_fields = ('created_at',)