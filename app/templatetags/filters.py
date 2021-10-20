from django.template.defaultfilters import register


@register.filter(name='dict_key')
def dict_key(d, k):
    """Returns the given key from a dictionary."""
    return d.get(k)


@register.filter(name='round')
def _round(f):
    """Returns the float f rounded to two decimal places and converted to a percentage String."""
    return str(int(round(f, 2)*100))