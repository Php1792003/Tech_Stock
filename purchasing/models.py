from django.db import models
from core.models import BaseModel
from assets.models import ComputerModel

class PurchaseInvoice(BaseModel):
    invoice_no = models.CharField(max_length=50, unique=True, verbose_name="Số hóa đơn")
    vendor = models.CharField(max_length=255, verbose_name="Nhà cung cấp")
    date = models.DateField(verbose_name="Ngày hóa đơn")
    total_amount = models.DecimalField(max_digits=18, decimal_places=0, default=0, verbose_name="Tổng tiền (VNĐ)")
    def __str__(self): return f"HĐ Mua hàng {self.invoice_no} - {self.vendor}"
    class Meta:
        verbose_name = "Hóa đơn mua hàng"; verbose_name_plural = "Hóa đơn mua hàng"

class PurchaseInvoiceLine(BaseModel):
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='lines', verbose_name="Hóa đơn gốc")
    computer_model = models.ForeignKey(ComputerModel, on_delete=models.PROTECT, verbose_name="Dòng máy")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    unit_price = models.DecimalField(max_digits=18, decimal_places=0, verbose_name="Đơn giá (VNĐ)")
    total_price = models.DecimalField(max_digits=18, decimal_places=0, editable=False, verbose_name="Thành tiền (VNĐ)")
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price; super().save(*args, **kwargs)
    def __str__(self): return f"{self.computer_model} (SL: {self.quantity})"
    class Meta:
        verbose_name = "Dòng HĐ mua hàng"; verbose_name_plural = "Dòng HĐ mua hàng"