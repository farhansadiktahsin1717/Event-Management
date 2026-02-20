from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group, User

ROLE_CHOICES = (
    ("Admin", "Admin"),
    ("Organizer", "Organizer"),
    ("Participant", "Participant"),
)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


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
