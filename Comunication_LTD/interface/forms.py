from django import forms
from config import password_pattern,min_password_length,forbidden_passwords
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import get_default_password_validators, password_validators_help_text_html


def is_common_password(password: str):
    if password in forbidden_passwords:
        raise ValidationError(
            ('Your password is too weak!'),
            params={'value': password},
        )
# TODO: Implement password history check, and login attempts
# TODO: shoot tuvia in the head

class LoginForm(forms.Form):
    username = forms.CharField(label=('Username'), widget=forms.TextInput(attrs={
        'placeholder':('Username'),
        'class': "form-control fadeIn second m-2 shadow-sm",
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='Username'"
    }))
    password = forms.CharField(label=('Password'), widget=forms.TextInput(attrs={
        'placeholder':('Password'),
        'class': 'form-control fadeIn second m-2 shadow-sm',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='password'",
        'type': 'password',
    }))



class registerForm(forms.Form):
    email = forms.CharField(label=('email'), widget=forms.TextInput(attrs={
        'placeholder':('Email'),
        'class': "form-control fadeIn second m-2 shadow-sm",
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='Email'"
    }))
    username = forms.CharField(label=('username'), widget=forms.TextInput(attrs={
        'placeholder':('username'),
        'class': "form-control fadeIn second m-2 shadow-sm",
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='username'"
    }))
    password = forms.CharField(validators=[is_common_password],min_length=min_password_length,label=('password'), widget=forms.TextInput(attrs={
        'placeholder':('Password'),
        'class': 'form-control fadeIn second m-2 shadow-sm',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='password'",
        'type': 'password',
        'pattern': password_pattern,
        'title': 'Use 8 or more characters with a mix of letters, numbers'
    }))



class SetPasswordForm2(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=("New password"),min_length=min_password_length,
        validators=[is_common_password],
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        #help_text=password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        min_length=min_password_length,
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        # validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user