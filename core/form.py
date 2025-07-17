from django import forms
from .models import DailyUsage

class DailyUsageForm(forms.ModelForm):
    class Meta:
        model = DailyUsage
        fields = ['date', 'icu_beds_used', 'oxy_cylinders']
