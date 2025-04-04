from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username
    
class LoanCalculation(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # Calculation type and subtype
    calculation_type = models.CharField(max_length=50, null=True, blank=True)  # 'interes' or 'series'
    calculation_subtype = models.CharField(max_length=50, null=True, blank=True)  # 'vp', 'vf', 'n', 'i', 'vencida', 'anticipada', 'perpetua', 'diferida'
    
    # Input values
    vf = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tasa = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    periodos = models.IntegerField(null=True, blank=True)
    renta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gracia = models.IntegerField(null=True, blank=True)

    # Result
    resultado = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.calculation_type} - {self.calculation_subtype} - {self.user.username} - {self.created_at}"