from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth import authenticate
from user_app.models import MyUser

from PIL import Image

# get custom user
User = get_user_model()


class MyUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


YEARS = [x for x in range(1960, 2021)]


class MyUserChangeForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ("username", "first_name", "last_name", "country", "city", "gender", 'profile_photo', 'birthday')
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "profile_photo": forms.FileInput(),
            "country": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "birthday": forms.SelectDateWidget(years=YEARS)

        }

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        """
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value
        """
        return self.initial["password"]


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput)


class Security(forms.Form):
    CurrentPassword = forms.CharField(widget=forms.PasswordInput(), label="Şifrə *")
    Newpassword = forms.CharField(widget=forms.PasswordInput(), label="Yeni Şifrə")
    ConfirmPassword = forms.CharField(widget=forms.PasswordInput(), label="Yeni Şifrə təkrar")
