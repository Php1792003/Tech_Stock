from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel


class Position(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên chức vụ")
    level = models.PositiveIntegerField(default=1, verbose_name="Cấp bậc")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Chức vụ"
        verbose_name_plural = "Các chức vụ"
        ordering = ['level', 'name']


class Department(BaseModel):
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã phòng ban")
    name = models.CharField(max_length=100, verbose_name="Tên phòng ban")
    manager = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='managed_department', verbose_name="Trưởng phòng")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Phòng ban"
        verbose_name_plural = "Các phòng ban"
        ordering = ['name']


class Employee(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Tài khoản")
    emp_code = models.CharField(max_length=20, unique=True, verbose_name="Mã nhân viên")
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Số điện thoại")
    position = models.ForeignKey(Position, on_delete=models.PROTECT, verbose_name="Chức vụ")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name="Phòng ban")
    is_active = models.BooleanField(default=True, verbose_name="Đang làm việc")

    def __str__(self):
        return f"{self.full_name} ({self.emp_code})"

    class Meta:
        verbose_name = "Nhân viên"
        verbose_name_plural = "Các nhân viên"
        ordering = ['full_name']