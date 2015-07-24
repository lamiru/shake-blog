import os
import uuid
from django.utils import timezone
from django.utils.encoding import force_text, smart_text


def random_name_upload_to(model_instance, filename):
    app_label = model_instance.__class__._meta.app_label
    model_cls_name = model_instance.__class__.__name__.lower()
    dirpath_format = app_label + '/' + model_cls_name + '/%Y/%m/%d'
    dirpath = os.path.normpath(force_text(timezone.now().strftime(smart_text(dirpath_format))))  # noqa
    random_name = uuid.uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return dirpath + '/' + random_name + extension
