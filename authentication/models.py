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
        unique=True,
        help_text=_("UUID `uuid4` random unique ID"),
    )
    alt_name = models.CharField(
        default="master",
        max_length=25,
        null=False,
        unique=True,
        editable=True,
        help_text=_("Alternative name")
    )
    email = models.EmailField(
        _("email address"),
        blank=False,
        unique=True,
        error_messages={
            "unique": _("This email address is already in use.")
        },
    )
    email_validated = models.BooleanField(
        default=False,
        help_text=_(
            "Whether the email address has been validated through the validation link"
        ),
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