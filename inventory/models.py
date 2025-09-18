from django.db import models
from django.conf import settings
from datetime import datetime

import assets
from core.models import BaseModel
from accounts.models import Department, Employee


class Location(BaseModel):
    class LocationType(models.TextChoices):
        WAREHOUSE = 'WAREHOUSE', 'Kho'
        DEPARTMENT = 'DEPARTMENT', 'Văn phòng/Phòng ban'
        VENDOR_REPAIR = 'VENDOR_REPAIR', 'Nhà cung cấp (Sửa chữa)'
        DISPOSAL = 'DISPOSAL', 'Nơi thanh lý'

    code = models.CharField(max_length=20, unique=True, verbose_name="Mã vị trí")
    name = models.CharField(max_length=100, verbose_name="Tên vị trí")
    type = models.CharField(max_length=20, choices=LocationType.choices, verbose_name="Loại vị trí")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name="Phòng ban liên quan")

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "Vị trí"
        verbose_name_plural = "Các vị trí"
        ordering = ['name']


class InventoryTxn(BaseModel):
    class TxnType(models.TextChoices):
        RECEIPT = 'RECEIPT', 'Nhập kho'
        ISSUE = 'ISSUE', 'Xuất cấp phát'
        RETURN = 'RETURN', 'Thu hồi/Trả về'
        TRANSFER = 'TRANSFER', 'Luân chuyển'
        REPAIR_OUT = 'REPAIR_OUT', 'Gửi đi sửa'
        REPAIR_IN = 'REPAIR_IN', 'Nhận về từ sửa chữa'
        WRITE_OFF = 'WRITE_OFF', 'Báo hỏng/Mất'
        DISPOSAL = 'DISPOSAL', 'Thanh lý'

    class TxnStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'Nháp'
        SUBMITTED = 'SUBMITTED', 'Đã gửi'
        APPROVED = 'APPROVED', 'Đã duyệt'
        REJECTED = 'REJECTED', 'Từ chối'
        POSTED = 'POSTED', 'Đã ghi sổ'

    code = models.CharField(max_length=30, unique=True, editable=False, verbose_name="Mã chứng từ")
    type = models.CharField(max_length=20, choices=TxnType.choices, verbose_name="Loại chứng từ")
    status = models.CharField(max_length=20, choices=TxnStatus.choices, default=TxnStatus.DRAFT,
                              verbose_name="Trạng thái CT")
    source_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='source_txns', null=True,
                                        blank=True, verbose_name="Nơi xuất")
    dest_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='dest_txns', null=True,
                                      blank=True, verbose_name="Nơi nhận")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True,
                                   verbose_name="Phòng ban yêu cầu")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_txns',
                                   verbose_name="Người tạo")
    issued_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='issued_txns', null=True, blank=True,
                                  verbose_name="Người xuất kho")
    received_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='received_txns', null=True,
                                    blank=True, verbose_name="Người nhận")
    approved_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='approved_txns', null=True,
                                    blank=True, verbose_name="Người duyệt")
    note = models.TextField(blank=True, verbose_name="Ghi chú")
    posted_at = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Ngày ghi sổ")

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            prefix_map = {'RECEIPT': 'PNK', 'ISSUE': 'PXK', 'RETURN': 'PTN', 'TRANSFER': 'PLC', 'REPAIR_OUT': 'PSC',
                          'REPAIR_IN': 'PNSC', 'WRITE_OFF': 'PBH', 'DISPOSAL': 'PTL'}
            prefix = prefix_map.get(self.type, 'CK')
            last_id = InventoryTxn.objects.last().id + 1 if InventoryTxn.objects.exists() else 1
            self.code = f"{prefix}-{datetime.now().strftime('%y%m%d')}-{last_id:04d}"
        super().save(*args, **kwargs)

    def process_transaction(self):
        if self.status != self.TxnStatus.POSTED or self.posted_at:
            raise ValueError("Chứng từ không hợp lệ hoặc đã được xử lý.")

        for line in self.lines.all():
            computer = line.computer
            line.prev_status = computer.status

            # Xử lý logic nghiệp vụ
            if self.type == self.TxnType.ISSUE:
                computer.status = assets.Computer.StatusChoices.ASSIGNED
                computer.current_location = self.dest_location
                computer.assigned_to = self.received_by
                computer.assigned_department = self.department
            elif self.type == self.TxnType.RETURN:
                computer.status = assets.Computer.StatusChoices.IN_STOCK
                computer.current_location = self.dest_location
                computer.assigned_to = None
                computer.assigned_department = None
            elif self.type == self.TxnType.DISPOSAL:
                computer.status = assets.Computer.StatusChoices.DISPOSED
                computer.current_location = self.dest_location
                computer.assigned_to = None
                computer.assigned_department = None
            # ... thêm các logic khác

            line.new_status = computer.status
            computer.save()
            line.save()

        self.posted_at = datetime.now()
        self.save()

    class Meta:
        verbose_name = "Chứng từ kho"
        verbose_name_plural = "Các chứng từ kho"


class InventoryTxnLine(BaseModel):
    inventory_txn = models.ForeignKey(InventoryTxn, on_delete=models.CASCADE, related_name='lines',
                                      verbose_name="Chứng từ gốc")
    computer = models.ForeignKey('assets.Computer', on_delete=models.PROTECT, verbose_name="Máy tính", related_name='history_lines')
    prev_status = models.CharField(max_length=20, blank=True, verbose_name="Trạng thái trước")
    new_status = models.CharField(max_length=20, blank=True, verbose_name="Trạng thái mới")
    note = models.CharField(max_length=255, blank=True, verbose_name="Ghi chú dòng")

    class Meta:
        verbose_name = "Dòng chứng từ"
        verbose_name_plural = "Các dòng chứng từ"
        unique_together = ('inventory_txn', 'computer')