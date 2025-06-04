from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone





# ============================
# Custom User Manager
# ============================

# Custom users management models
class CustomUserManager(BaseUserManager):
    # Standard user model
    def create_user(self, email, first_name, last_name, address, password=None, **extra_fields):
        # Validates that an email is provided
        if not email:
            raise ValueError("Users must provide an email address")
        
        # Lowercase the email format
        email = self.normalize_email(email)

        # Creates a user instance with the given data
        user = self.model(email=email, first_name=first_name, last_name=last_name, address=address, **extra_fields)

        # Hashes and sets the password
        user.set_password(password)

        # Saves the user to the database
        user.save(using=self._db)

        # Return
        return user

    # Super user model
    def create_superuser(self, email, first_name, last_name, address, password=None, **extra_fields):

        # Sets default fields required for a superuser
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Validates that a password is provided
        if not password:
            raise ValueError("Superusers must have a password.")
        
        # Reuses create_user to build the superuser
        return self.create_user(email, first_name, last_name, address, password, **extra_fields)





# ============================
# Custom User Model
# ============================

#Custom users model
class CustomUser(AbstractBaseUser, PermissionsMixin):

    # Email field used as the unique identifier for authentication
    email = models.EmailField(unique=True)

    # Stores the user's first name
    first_name = models.CharField(max_length=50)

    # Stores the user's last name
    last_name = models.CharField(max_length=50)

    # Stores the user's postal address
    address = models.TextField()

    # Indicates if the user's account is active
    is_active = models.BooleanField(default=True)

    # Grants staff-level access to the admin panel
    is_staff = models.BooleanField(default=False)

    # Timestamp for when the account was created
    date_joined = models.DateTimeField(default=timezone.now)

    # Assigns the custom user manager for user creation logic
    objects = CustomUserManager()

    # Specifies email as the field used for login
    USERNAME_FIELD = "email"

    # Fields required when creating a superuser
    REQUIRED_FIELDS = ["first_name", "last_name", "address"]

    def __str__(self):

        # Returns the email as the string representation of the user
        return self.email
