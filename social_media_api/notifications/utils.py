from django.contrib.contenttypes.models import ContentType
from django.apps import apps

def create_notification(*, recipient, actor, verb, target=None):
    # Resolve model at call time to avoid import-time circulars
    Notification = apps.get_model("notifications", "Notification")

    ct = None
    obj_id = None
    if target is not None:
        ct = ContentType.objects.get_for_model(target.__class__)
        obj_id = target.pk

    return Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type=ct,
        target_object_id=obj_id,
    )
