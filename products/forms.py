from django import forms
from .models import Review


# =======================================================
# REVIEW FORM
# =======================================================

# This form allows users to submit a rating and optional comment for a specific service
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

        # Input widgets for each field
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'placeholder': 'Enter a rating from 1 to 5'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your review here...',
                'rows': 4,
            }),
        }

        # User friendly field labels in British English
        labels = {
            'rating': 'Your Rating (1 to 5)',
            'comment': 'Your Feedback',
        }