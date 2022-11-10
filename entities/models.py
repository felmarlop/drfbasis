import uuid

from authentication.models import User
from django.db import models
from django.utils.translation import gettext as _


class BaseEntity(models.Model):
    """Abstract class to be extended for each entity"""

    created = models.DateTimeField(
        auto_now_add=True,
        help_text="Records when the object was added to the database"
    )
    updated = models.DateTimeField(
        auto_now=True,
        help_text="Records when the object was last updated"
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        app_label = "entities"

    @classmethod
    def getobj(cls, id):
        """Retrieve an object from the db by it's unique id"""
        return cls.objects.get(id=id)


class Entity(BaseEntity):
    name = models.CharField(
        max_length=150,
        blank=False,
        help_text=_("No empty name for a entity")
    )

    link = models.URLField(
      default=None,
      max_length=200,
      blank=False,
      unique=True,
      help_text=_("Unique link for a entity")
    )

    views = models.PositiveIntegerField(
      default=0,
      help_text=_("Number of views of a entity"),
    )

    class Meta:
        app_label = "entities"
        ordering = ["views"]
        
    
    