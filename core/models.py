from django.db import models





# =======================================================
# CONTACT MESSAGE MODEL
# =======================================================

# Stores enquiries submitted via the contact form
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Returns a readable string representation for admin
    def __str__(self):
        return f"{self.name} ({self.email})"
