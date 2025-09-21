# assets/models.py (PHIÊN BẢN HOÀN CHỈNH)

from django.db import models
from core.models import BaseModel
from accounts.models import Employee, Department

class ComputerModel(BaseModel):
    # ĐÃ THÊM: Các trường cần thiết cho model này
    brand = models.CharField(max_length=100, verbose_name="Hãng sản xuất")
    model = models.CharField(max_length=100, verbose_name="Tên dòng máy")
    cpu = models.CharField(max_length=100, blank=True, verbose_name="CPU")
    ram_gb = models.PositiveIntegerField(blank=True, null=True, verbose_name="RAM (GB)")
    storage = models.CharField(max_length=100, blank=True, verbose_name="Ổ cứng")
    gpu = models.CharField(max_length=100, blank=True, verbose_name="GPU")
    os = models.CharField(max_length=50, blank=True, verbose_name="Hệ điều hành")
    notes = models.TextField(blank=True, verbose_name="Ghi chú thêm")

    def __str__(self):
        return f"{self.brand} {self.model}"

    class Meta:
        verbose_name = "Dòng máy tính"
        verbose_name_plural = "Các dòng máy tính"
        unique_together = ('brand', 'model')
        ordering = ['brand', 'model']


class Computer(BaseModel):
    class StatusChoices(models.TextChoices):
        IN_STOCK = 'IN_STOCK', 'Trong kho'
        ASSIGNED = 'ASSIGNED', 'Đã cấp phát'
        RESERVED = 'RESERVED', 'Đã đặt trước'
        REPAIR = 'REPAIR', 'Đang sửa chữa'
        RETIRED = 'RETIRED', 'Đã bán/Cho đi'
        DISPOSED = 'DISPOSED', 'Đã thanh lý'

    asset_tag = models.CharField(max_length=50, unique=True, verbose_name="Mã tài sản")
    serial = models.CharField(max_length=100, unique=True, verbose_name="Số serial")
    computer_model = models.ForeignKey(ComputerModel, on_delete=models.PROTECT, verbose_name="Dòng máy")
    purchase_date = models.DateField(null=True, blank=True, verbose_name="Ngày mua")
    warranty_expiry = models.DateField(null=True, blank=True, verbose_name="Ngày hết hạn BH")
    purchase_price = models.DecimalField(max_digits=18, decimal_places=0, default=0, verbose_name="Giá mua (VNĐ)")
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.IN_STOCK,
                              verbose_name="Trạng thái")
    current_location = models.ForeignKey('inventory.Location', on_delete=models.PROTECT, verbose_name="Vị trí hiện tại")
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name="Người sử dụng")
    assigned_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                            verbose_name="Phòng ban sử dụng")
    remark = models.TextField(blank=True, verbose_name="Ghi chú/Lý do")

    useful_life = models.PositiveIntegerField(
        default=3,
        verbose_name="Vòng đời sử dụng (năm)"
    )
    salvage_value = models.DecimalField(
        max_digits=18,
        decimal_places=0,
        default=0,
        verbose_name="Giá trị thanh lý ước tính (VNĐ)"
    )

    def __str__(self):
        return f"{self.computer_model} ({self.asset_tag})"

    class Meta:
        verbose_name = "Máy tính"
        verbose_name_plural = "Danh sách máy tính"
        ordering = ['-purchase_date', 'asset_tag']