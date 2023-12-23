from django import forms
from .models import SupportContact

class SupportContactForm(forms.ModelForm):
    class Meta:
        model = SupportContact
        fields = ['full_name', 'phone_number', 'subject', 'email', 'message']
