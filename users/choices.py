from django.db import models
from django.utils.translation import gettext_lazy as _


class Roles(models.TextChoices):
    ADMIN = 'admin', _("Admin")
    MANAGER = 'manager', _("Manager")
    CLIENT = 'client', _("Client")

class OrderStatus(models.TextChoices):
    DRAFT = 'draft', _("Draft")
    APPROVED = 'approved', _('Аpproved')
    PAID = 'paid', _('Paid')
    COMPLETED = 'completed', _('Completed')
    CANCELLED = 'cancelled', _('Cancelled')

class PaymentMethod(models.TextChoices):
    CASH = 'cash', _('Cash')
    CARD = 'card', _('Card')