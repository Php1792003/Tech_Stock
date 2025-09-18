from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import SalesInvoiceLine

@receiver([post_save, post_delete], sender=SalesInvoiceLine)
def update_invoice_total_amount(sender, instance, **kwargs):
    invoice = instance.invoice
    total = invoice.lines.aggregate(total=Sum('total_price'))['total'] or 0
    invoice.total_amount = total
    invoice.save()