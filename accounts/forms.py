from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        label=_("Email address")
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        label=_("First name")
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        label=_("Last name")
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': _("Username"),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("This email address is already registered."))
        return email