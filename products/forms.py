from django import forms
from .models import Review


# =======================================================
# REVIEW FORM
# =======================================================

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
            'rating': forms.RadioSelect(choices=[
                (1, '★☆☆☆☆'),
                (2, '★★☆☆☆'),
                (3, '★★★☆☆'),
                (4, '★★★★☆'),
                (5, '★★★★★'),
            ]),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your review here...',
                'rows': 4,
            }),
        }

        # Field labels in British English
        labels = {
            'rating': 'Your Rating',
            'comment': 'Your Feedback',
        }