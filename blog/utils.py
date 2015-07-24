import os
import uuid
from io import BytesIO as StringIO
from PIL import Image, ImageOps
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


def pil_image(input_f, quality=80):
    if isinstance(input_f, str):
        filename = input_f
    elif hasattr(input_f, 'name'):
        filename = input_f.name
    else:
        filename = 'noname.png'

    extension = os.path.splitext(filename)[-1].lower()
    try:
        format = {
            '.jpg': 'jpeg',
            '.jpeg': 'jpeg',
            '.png': 'png',
            '.gif': 'gif',
        }[extension]
    except KeyError:
        format = 'png'

    image = Image.open(input_f)
    return image, format


def image_to_file(image, format, quality):
    output_f = StringIO()
    image.save(output_f, format=format, quality=quality)
    output_f.seek(0)
    return output_f


def thumbnail(input_f, width, height, quality=80):
    image, format = pil_image(input_f, quality)
    image.thumbnail((width, height), Image.ANTIALIAS)
    return image_to_file(image, format, quality)


def square_image(input_f, max_size, quality=80):
    image, format = pil_image(input_f, quality)
    max_size = min(image.size[0], image.size[1], max_size)
    image = ImageOps.fit(image, size=(max_size, max_size))
    return image_to_file(image, format, quality)
