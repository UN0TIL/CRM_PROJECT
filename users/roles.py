from django.db import models
from django.utils.translation import gettext_lazy as _


class Roles(models.TextChoices):
    ADMIN = 'admin', _("Admin")
    MANAGER = 'manager', _("Manager")
    CLIENT = 'client', _("Client")
