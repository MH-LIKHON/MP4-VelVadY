from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator





# =======================================================
# SERVICE MODEL FOR DIGITAL PRODUCTS / SERVICES
# =======================================================

# Models for digital products and services
class Service(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # New category field with predefined choices for MP4 distinction
    CATEGORY_CHOICES = [
        ('Design', 'Design'),
        ('Business', 'Business'),
        ('Tech', 'Tech'),
        ('Writing', 'Writing'),
        ('Marketing', 'Marketing'),
    ]

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Design',
        help_text='Select a category for this service.'
    )

    # Automatically generates a slug from the title if one is not set
    def save(self, *args, **kwargs):
        """
        Overrides the default save method to automatically create a slug from the title
        if no slug value is provided before saving the service instance.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # Returns the service title when the object is printed
    def __str__(self):
        """
        Returns a human-readable string representation of the service object,
        which will appear in admin panels and other debug outputs.
        """
        return self.title





# =======================================================
# REVIEW MODEL
# =======================================================

# This model stores user-submitted reviews for each service
class Review(models.Model):
    # Each review is linked to one service
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')

    # Each review is submitted by a registered user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Rating must be between 1 and 5
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    # Optional text comment provided by the user
    comment = models.TextField(blank=True)

    # Timestamp for when the review was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Show reviewer and rating when listing reviews in admin
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email} - {self.rating}★"
    




# =======================================================
# PURCHASE MODEL
# =======================================================

# Stores each successful service purchase
class Purchase(models.Model):
    """
    Represents a record of a completed service purchase by a user via Stripe.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    stripe_session_id = models.CharField(max_length=255, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.email} purchased {self.service.title} for £{self.amount_paid}'