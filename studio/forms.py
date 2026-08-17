from django import forms
from django.utils import timezone
from .models import Booking, ContactMessage, Service


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["full_name", "phone", "email", "service", "preferred_date",
                  "preferred_time", "location_preference", "notes"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your full name", "class": "form-control"}),
            "phone": forms.TextInput(attrs={"placeholder": "e.g. 98765 43210", "class": "form-control"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "class": "form-control"}),
            "service": forms.Select(attrs={"class": "form-control"}),
            "preferred_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "preferred_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "location_preference": forms.Select(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell us about your event, look preferences, etc.",
                                            "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].queryset = Service.objects.filter(is_active=True).order_by("category__order", "order")
        self.fields["service"].empty_label = "Select a service"
        self.fields["email"].required = False

    def clean_preferred_date(self):
        date = self.cleaned_data["preferred_date"]
        if date < timezone.localdate():
            raise forms.ValidationError("Please choose a date from today onward.")
        return date


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "class": "form-control"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "class": "form-control"}),
            "phone": forms.TextInput(attrs={"placeholder": "Optional", "class": "form-control"}),
            "subject": forms.TextInput(attrs={"placeholder": "Subject", "class": "form-control"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "How can we help?", "class": "form-control"}),
        }
