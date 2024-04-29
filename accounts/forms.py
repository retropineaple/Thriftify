from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Item
from django.contrib.auth.forms import PasswordChangeForm
from .models import Message


class MinimalSignupForm(UserCreationForm):
    username = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password1 = forms.CharField(
        label="", widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Password confirmation"}),
    )
    phone_number = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Phone Number"})
    )
    email = forms.EmailField(
        label="", widget=forms.EmailInput(attrs={"placeholder": "Email"})
    )
    name = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Name"})
    )
    roll_number = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Roll Number"})
    )

    class Meta:
        model = User
        fields = [
            "name",
            "roll_number",
            "phone_number",
            "email",
            "username",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()

        phone_number = self.cleaned_data["phone_number"]
        email = self.cleaned_data["email"]
        name = self.cleaned_data["name"]
        roll_number = self.cleaned_data["roll_number"]
        UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            email=email,
            name=name,
            roll_number=roll_number,
        )

        return user


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["name", "phone_number", "email", "roll_number"]


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="", widget=forms.PasswordInput(attrs={"placeholder": "Old Password"})
    )
    new_password1 = forms.CharField(
        label="", widget=forms.PasswordInput(attrs={"placeholder": "New Password"})
    )
    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "New Password confirmation"}),
    )


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "price", "picture", "description"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]
