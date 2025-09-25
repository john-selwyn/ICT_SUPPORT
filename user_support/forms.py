from django import forms
from .models import SupportRequest

class SupportRequestForm(forms.ModelForm):
    class Meta:
        model = SupportRequest
        fields = ["name", "unit", "email", "contact", "category", "description", "status", "process"]
