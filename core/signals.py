from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.contrib.contenttypes.models import ContentType
from audit.models import AuditLog
from accounts.models import Position, Department, Employee
TRACKED_MODELS = [Position, Department, Employee]
import threading
_thread_locals = threading.local()
from .middleware import CurrentUserMiddleware


@receiver(pre_save)
def capture_old_data(sender, instance, **kwargs):
    if sender in TRACKED_MODELS and instance.pk:
        try:
            instance._old_state = model_to_dict(sender.objects.get(pk=instance.pk))
        except sender.DoesNotExist:
            instance._old_state = None


@receiver(post_save)
def log_create_update(sender, instance, created, **kwargs):
    if sender not in TRACKED_MODELS:
        return

    user = CurrentUserMiddleware.get_current_user()
    action = AuditLog.ActionChoices.CREATE if created else AuditLog.ActionChoices.UPDATE

    before_data = None
    if not created and hasattr(instance, '_old_state') and instance._old_state:
        before_data = instance._old_state

    after_data = model_to_dict(instance)

    if before_data == after_data:
        return

    AuditLog.objects.create(
        changed_by=user, action=action,
        object_type=ContentType.objects.get_for_model(instance), object_id=instance.pk,
        before=before_data, after=after_data
    )


@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender not in TRACKED_MODELS:
        return

    user = CurrentUserMiddleware.get_current_user()
    AuditLog.objects.create(
        changed_by=user, action=AuditLog.ActionChoices.DELETE,
        object_type=ContentType.objects.get_for_model(instance), object_id=instance.pk,
        before=model_to_dict(instance), after=None
    )