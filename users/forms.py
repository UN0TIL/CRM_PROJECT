from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CustomUser
from .roles import Roles

class UserCreateForm(forms.ModelForm):
    email = forms.EmailField(max_length=30)
    is_active = forms.BooleanField(initial=True)
    # is_staff = forms.BooleanField(initial=False)
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'role', 'is_active', 'is_staff']

    def clean(self):
        data = super().clean()

        password1 = data['password1']
        password2 = data['password2']

        if password1 != password2:
            raise forms.ValidationError(_("passwords don't match"))
        
        return data
        

    def save(self, commit=True):
        user = super().save(commit=False)
        data = self.cleaned_data

        user.set_password(data['password1'])
        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    email = forms.EmailField(max_length=30)
    role = forms.CharField(max_length=10)
    is_active = forms.BooleanField()
    is_staff = forms.BooleanField()

    class Meta:
        model = CustomUser
        fields = ['email', 'role', 'is_active', 'is_staff']
