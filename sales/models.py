from django.db import models
from django.utils import timezone
from core.models import BaseModel

from assets.models import Computer
from accounts.models import Employee


class SalesInvoice(BaseModel):
    invoice_no = models.CharField(max_length=50, unique=True, verbose_name="Số hóa đơn")
    customer = models.CharField(max_length=255, verbose_name="Khách hàng")
    date = models.DateField(verbose_name="Ngày hóa đơn")
    total_amount = models.DecimalField(max_digits=18, decimal_places=0, default=0, verbose_name="Tổng doanh thu (VNĐ)")

    created_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='sales_invoices',
        verbose_name="Nhân viên bán hàng",
        editable=False
    )

    def __str__(self): return f"HĐ Bán hàng {self.invoice_no} - {self.customer}"

    class Meta:
        verbose_name = "Hóa đơn bán hàng"
        verbose_name_plural = "Hóa đơn bán hàng"


class SalesInvoiceLine(BaseModel):
    invoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE, related_name='lines',
                                verbose_name="Hóa đơn gốc")
    computer = models.ForeignKey(Computer, on_delete=models.PROTECT, verbose_name="Máy tính bán ra")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    unit_price = models.DecimalField(max_digits=18, decimal_places=0, verbose_name="Đơn giá bán (VNĐ)")
    total_price = models.DecimalField(max_digits=18, decimal_places=0, editable=False, verbose_name="Thành tiền (VNĐ)")
    cost_allocated = models.DecimalField(max_digits=18, decimal_places=0, editable=False,
                                         verbose_name="Giá vốn phân bổ (VNĐ)")

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        if self.computer:
            self.cost_allocated = self.computer.purchase_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self): return f"{self.computer} (Giá bán: {self.unit_price})"

    class Meta:
        verbose_name = "Dòng HĐ bán hàng"
        verbose_name_plural = "Dòng HĐ bán hàng"