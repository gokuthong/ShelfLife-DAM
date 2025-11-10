from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with role-based permissions
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    )

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

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_admin(self):
        """Check if user has admin role"""
        return self.role == 'admin' or self.is_superuser

    @property
    def is_editor(self):
        """Check if user has editor role or higher"""
        return self.role in ['admin', 'editor'] or self.is_superuser

    @property
    def is_viewer(self):
        """Check if user has viewer role (all authenticated users)"""
        return self.role in ['admin', 'editor', 'viewer'] or self.is_superuser
