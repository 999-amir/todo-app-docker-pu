from django import forms
from .models import CostumeUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class CostumeUserCreationForm(forms.ModelForm):
    password_1 = forms.CharField(
        widget=forms.PasswordInput, label="password_1"
    )
    password_2 = forms.CharField(
        widget=forms.PasswordInput, label="password_2"
    )

    class Meta:
        model = CostumeUser
        fields = ("email",)

    def clean(self):
        cd = super().clean()
        password_1, password_2 = cd.get("password_1"), cd.get("password_2")
        if password_1 and password_2 and password_1 != password_2:
            raise ValidationError("!!! password are not the same !!!")
        elif len(password_1) < 4:
            raise ValidationError("password should be more than 4 char")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password_1"])
        if commit:
            user.save()
        return user


class CostumeUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='want to change password? <a href="../password/">click here</a>'
    )

    class Meta:
        model = CostumeUser
        fields = ("email",)


class SignupForm(forms.Form):
    attrs = {
        "class": "mb-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    }

    email = forms.CharField(widget=forms.EmailInput(attrs=attrs))
    password_1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs))
    password_2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs))

    def clean(self):
        cd = super().clean()
        password_1, password_2 = cd.get("password_1"), cd.get("password_2")
        if password_1 and password_2:
            if password_1 != password_2:
                raise ValidationError("! passwords are not the same !")
            elif len(password_1) < 4:
                raise ValidationError(
                    "! password should be more than 4 char !"
                )
        else:
            raise ValidationError("! password should be added !")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if CostumeUser.objects.filter(email=email).exists():
            raise ValidationError("! this email has been registered before !")
        return email


class LoginForm(forms.Form):
    attrs = {
        "class": "mb-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    }

    email = forms.CharField(widget=forms.EmailInput(attrs=attrs))
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs))


class ProfileForm(forms.Form):
    f_name = forms.CharField(widget=forms.TextInput)
    l_name = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.TextInput)


class ProfileDescriptionForm(forms.Form):
    description = forms.CharField(widget=forms.TextInput)
