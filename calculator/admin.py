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
    list_display = ('user', 'amount', 'interest_rate', 'term_months', 'monthly_payment', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at', 'interest_rate')