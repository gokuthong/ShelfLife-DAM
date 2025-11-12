from django.contrib.auth.models import AbstractUser
from django.db import models
<<<<<<< HEAD


class User(AbstractUser):
    """
    Custom User model with role-based permissions
    """
=======
import uuid


def avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"avatars/{instance.id}/{filename}"


class User(AbstractUser):
>>>>>>> 3068d61 (advanced filters, comments CRUD, and role-based permissions)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    )

<<<<<<< HEAD
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='viewer',
        help_text='User role determines access permissions'
    )
    profile_info = models.TextField(blank=True, null=True, help_text='Additional profile information')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        db_table = 'users'
        ordering = ['-date_joined']
=======
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')
    profile_info = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)

    class Meta:
        db_table = 'users'

    def save(self, *args, **kwargs):
        # Automatically set superusers and staff as admin role
        if self.is_superuser or self.is_staff:
            self.role = 'admin'
        super().save(*args, **kwargs)
>>>>>>> 3068d61 (advanced filters, comments CRUD, and role-based permissions)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
<<<<<<< HEAD
    def is_admin(self):
        """Check if user has admin role"""
=======
    def avatar_url(self):
        return self.avatar.url if self.avatar else None

    @property
    def is_admin(self):
>>>>>>> 3068d61 (advanced filters, comments CRUD, and role-based permissions)
        return self.role == 'admin' or self.is_superuser

    @property
    def is_editor(self):
<<<<<<< HEAD
        """Check if user has editor role or higher"""
        return self.role in ['admin', 'editor'] or self.is_superuser

    @property
    def is_viewer(self):
        """Check if user has viewer role (all authenticated users)"""
        return self.role in ['admin', 'editor', 'viewer'] or self.is_superuser
=======
        return self.role == 'editor'

    @property
    def is_viewer(self):
        return self.role == 'viewer'
>>>>>>> 3068d61 (advanced filters, comments CRUD, and role-based permissions)
