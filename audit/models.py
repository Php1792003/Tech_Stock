from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.models import BaseModel

class AuditLog(BaseModel):
    class ActionChoices(models.TextChoices):
        CREATE = 'CREATE', 'Tạo mới'
        UPDATE = 'UPDATE', 'Cập nhật'
        DELETE = 'DELETE', 'Xóa'
        STATUS_CHANGE = 'STATUS_CHANGE', 'Thay đổi trạng thái'

    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Người thay đổi")
    action = models.CharField(max_length=20, choices=ActionChoices.choices, verbose_name="Hành động")
    object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Loại đối tượng")
    object_id = models.PositiveIntegerField(verbose_name="ID đối tượng")
    target_object = GenericForeignKey('object_type', 'object_id')
    before = models.JSONField(null=True, blank=True, verbose_name="Dữ liệu trước")
    after = models.JSONField(null=True, blank=True, verbose_name="Dữ liệu sau")

    def __str__(self):
        return f"{self.get_action_display()} on {self.target_object} by {self.changed_by}"

    class Meta:
        verbose_name = "Nhật ký thay đổi"
        verbose_name_plural = "Nhật ký thay đổi"