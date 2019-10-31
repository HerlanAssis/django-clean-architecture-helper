from django.utils import six
from django.utils.encoding import force_text
from django.utils.functional import Promise
from graphene.utils.str_converters import to_camel_case


def isiterable(value):
    try:
        iter(value)
    except TypeError:
        return False
    return True


def _camelize_django_str(s):
    if isinstance(s, Promise):
        s = force_text(s)
    return to_camel_case(s) if isinstance(s, six.string_types) else s


def camelize(data):
    if isinstance(data, dict):
        return {_camelize_django_str(k): camelize(v) for k, v in data.items()}
    if isiterable(data) and not isinstance(data, (six.string_types, Promise)):
        return [camelize(d) for d in data]
    return data
