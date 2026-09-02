from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="البريد الإلكتروني")
    first_name = forms.CharField(max_length=30, required=True, label="الاسم الأول")
    last_name = forms.CharField(max_length=30, required=True, label="الاسم الأخير")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("هذا البريد الإلكتروني مُسجل بالفعل.")
        return email