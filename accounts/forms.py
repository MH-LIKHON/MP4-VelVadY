from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import CustomUser

# ============================
# Registration Form
# ============================
class CustomUserRegistrationForm(UserCreationForm):
    # Additional field: Terms and Conditions agreement
    terms = forms.BooleanField(
        label="I agree to the Terms and Conditions",
        error_messages={"required": "You must agree to the terms to register."}
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "address", "password1", "password2", "terms"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # I am customising form field labels and placeholders for clarity
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter your first name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter your last name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Your email address'})
        self.fields['address'].widget.attrs.update({'placeholder': 'Full postal address'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create a strong password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your password'})





# =======================================================
# PROFILE UPDATE FORM
# =======================================================

# ------------------------------- Form to update user's profile -------------------------------
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'address']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full postal address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email
