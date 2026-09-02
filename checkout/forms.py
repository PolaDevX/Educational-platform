from django import forms
from django.utils.translation import gettext as _

class UserInfoForm(forms.Form):
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()