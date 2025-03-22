from kapita.core.data.enum.base import BaseStrEnum


class SystemNotificationType(BaseStrEnum):
    order_new = "order_new"
    order_repayment_change = "order_repayment_change"
    order_repayment_new = "order_repayment_new"
