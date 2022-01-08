import time

from django.template.defaultfilters import register


@register.filter(name='dict_key')
def dict_key(d, k):
    """Returns the given key from a dictionary."""
    return d.get(k)


@register.filter(name='round')
def _round(f):
    """Returns the float f rounded to two decimal places and converted to a percentage String."""
    return str(int(round(f, 2) * 100))


@register.filter(name='format_time')
def format_time(unix_time):
    """Returns a string in form of 'dd.mm.yyyy hh:mm' for a given unix time stamp."""
    if unix_time is None:
        return "-"
    return time.strftime('%d %B %Y %H:%M', time.localtime(int(unix_time)))


@register.filter(name='currency')
def format_currency(amount):
    """Returns a string that represents a number in a readable format.
    Input: 1920374
    Output: 1.920.374
    """
    if amount is None:
        return "-"
    return "{:,}".format(amount)


@register.filter('time')
def format_seconds(seconds):
    """Returns a String in the form of '00h 00m 00s' for a given integer that represents a time delta in seconds."""
    if seconds is None:
        return "-"
    if seconds < 60:
        return "{}s".format(seconds)
    minutes = seconds // 60
    seconds = seconds % 60
    if minutes < 60:
        return "{}m {}s".format(minutes, seconds)
    hours = minutes // 60
    minutes = minutes % 60
    return "{}h {}m {}s".format(hours, minutes, seconds)


@register.filter('css_color_class')
def css_color_class(value):
    """Returns a CSS class name for a given value."""
    if value is None or float(value) == 0:
        return ""
    if float(value) < 0:
        return "negative"
    return "positive"


@register.filter('css_color_class_from_dict')
def css_color_class_from_dict(d, k):
    """Returns a CSS class name for a given dict and key."""
    return css_color_class(d.get(k))


@register.filter('bold_if_true')
def bold_if_true(value):
    """Returns a bolded string for a given boolean value."""
    if value == True:
        return "bold"
    return ""
