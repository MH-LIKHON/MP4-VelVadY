from django import forms
from .models import CustomUser
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm






# ============================
# Registration Form
# ============================

# Handles new user registration
class CustomUserRegistrationForm(UserCreationForm):
    # Additional field for terms and conditions agreement
    terms = forms.BooleanField(
    label=mark_safe('I agree to the <a href="/legal/" target="_blank">Terms & Privacy</a>'),
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

# Handles registered users information changes
class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating the user's profile fields including name, email, and address.
    """

    class Meta:
        # This form is linked to the CustomUser model
        model = CustomUser

        # The fields to display and update in the form
        fields = ['first_name', 'last_name', 'email', 'address']

        # Customise input fields with Bootstrap classes and placeholders
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Full postal address'
            }),
        }

    # Email Uniqueness Validation
    def clean_email(self):
        """
        Ensures the email entered is not already used by another user in the system,
        excluding the current user’s email to allow unchanged entries.
        """
        email = self.cleaned_data.get('email')
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email