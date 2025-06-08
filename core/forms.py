from django import forms
from .models import ContactMessage

# =======================================================
# CONTACT FORM FOR ENQUIRIES
# =======================================================

# Contact form structure using the ContactMessage model
class ContactForm(forms.ModelForm):
    """
    Form for users to submit a message via the contact page.
    """

    # Defines which model and fields the form will use
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

        # Customises form field appearance with Bootstrap styling
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Type your message here...',
                'rows': 5
            }),
        }
