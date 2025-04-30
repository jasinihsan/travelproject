from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.accounts.models import CustomUser


REGISTER_USER_TYPE_CHOICES = [
    ('vendor','Vendor'),
    ('customer','Customer'),
]
class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=REGISTER_USER_TYPE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ["full_name", "email", "user_type", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data["user_type"] 
        if commit:
            user.save()
        return user


class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["full_name", "email", "user_type"]


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'autocomplete': 'new-password',
            'class': 'form-control'
        })
    )
    user_type = forms.ChoiceField(choices=REGISTER_USER_TYPE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ["full_name", "email", "password", "user_type"]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Enter full name',
                'autocomplete': 'off'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter email',
                'autocomplete': 'off'
            }),
            'user_type': forms.Select(attrs={
                'autocomplete': 'off'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  
        user.user_type = self.cleaned_data["user_type"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
            'placeholder': 'Enter email'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Email"
        self.fields['username'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
            'placeholder': 'Enter email'
        })


    def clean_username(self):
        return self.cleaned_data["username"].lower()
