from django.db import models
from django.contrib.auth.models import User

class DailyUsage(models.Model):
    date = models.DateField()
    
    icu_beds_used = models.PositiveIntegerField()
    oxy_cylinders = models.PositiveBigIntegerField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.date} - ICU: {self.icu_beds_used}"
