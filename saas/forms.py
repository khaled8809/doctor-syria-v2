from django import forms

from .models import Tenant


class TenantRegistrationForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ["name", "subdomain"]

    def clean_subdomain(self):
        subdomain = self.cleaned_data["subdomain"].lower()
        if Tenant.objects.filter(subdomain=subdomain).exists():
            raise forms.ValidationError("This subdomain is already taken.")
        return subdomain
