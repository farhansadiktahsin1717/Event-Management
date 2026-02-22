from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group

User = get_user_model()

ROLE_CHOICES = (
    ("Admin", "Admin"),
    ("Organizer", "Organizer"),
    ("Participant", "Participant"),
)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    phone_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone_number", "profile_picture")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "w-full rounded-lg border border-slate-300 px-3 py-2"}),
            "last_name": forms.TextInput(attrs={"class": "w-full rounded-lg border border-slate-300 px-3 py-2"}),
            "email": forms.EmailInput(attrs={"class": "w-full rounded-lg border border-slate-300 px-3 py-2"}),
            "phone_number": forms.TextInput(
                attrs={"class": "w-full rounded-lg border border-slate-300 px-3 py-2", "placeholder": "+1 555 123 4567"}
            ),
            "profile_picture": forms.ClearableFileInput(attrs={"class": "w-full rounded-lg border border-slate-300 px-3 py-2"}),
        }

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if not email:
            raise forms.ValidationError("Email is required.")

        qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name",)


class RoleUpdateForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    def clean_user_id(self):
        user_id = self.cleaned_data["user_id"]
        if not User.objects.filter(pk=user_id).exists():
            raise forms.ValidationError("Invalid user selected.")
        return user_id
