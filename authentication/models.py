import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    """Main app user, extending default Django users."""

    uid = models.CharField(
        max_length=40,
        null=True,
        editable=False,
        unique=True
    )
    alt_name = models.CharField(
        default="master",
        max_length=25,
        null=False,
        unique=True,
        editable=True
    )
    i_alt_name = models.CharField(
        default="master",
        max_length=25,
        null=False,
        unique=True,
        editable=True
    )
    email = models.EmailField(
        _("email address"),
        blank=False,
        unique=True
    )
    email_validated = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.id}: {self.username} - {self.email}"

    class Meta:
        app_label = "authentication"
        ordering = ["id"]

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = str(uuid.uuid4())
        super().save(*args, **kwargs)