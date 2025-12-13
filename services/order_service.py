from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..users.choices import OrderStatus
from ..users.models import CustomUser, Order

ALLOWED_STATUS_TRANSITIONS = {
    OrderStatus.DRAFT: {
        OrderStatus.APPROVED,
        OrderStatus.CANCELLED,
    },
    OrderStatus.APPROVED: {
        OrderStatus.PAID,
        OrderStatus.CANCELLED,
    },
    OrderStatus.PAID: {
        OrderStatus.COMPLETED,
    },
    OrderStatus.COMPLETED: set(),
    OrderStatus.CANCELLED: set(),
}

class OrderService:

    @staticmethod
    def change_status(order: Order, new_status: str, user: CustomUser):
        current_status = order.status

        if new_status not in ALLOWED_STATUS_TRANSITIONS[current_status]:
            raise ValidationError(
                _("Can't change status from %(from)s to %(to)s") % {
                    "from": current_status,
                    "to": new_status
                }
            )

        # проверка прав
        if not OrderService.can_user_change_status(order, user, new_status):
            raise ValidationError(_('Insufficient rights'))

        order.status = new_status
        order.save(update_fields=['status', 'updated_at'])

        return order
    
    @staticmethod
    def can_user_change_status(order: Order, user: CustomUser, new_status: str) -> bool:
        # админ может всё
        if user.is_superuser:
            return True

        # менеджер заказа
        if user == order.manager:
            return True

        # клиент не может менять статус
        return False