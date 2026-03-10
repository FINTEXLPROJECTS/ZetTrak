from django import template

register = template.Library()

@register.filter
def split(value, arg):
    return value.split(arg)

@register.filter
def get_item(dictionary, key):
    if not dictionary:
        return None
    res = dictionary.get(key)
    if res is None:
        try:
            res = dictionary.get(int(key))
        except (ValueError, TypeError):
            pass
    if res is None:
        try:
            res = dictionary.get(str(key))
        except (ValueError, TypeError):
            pass
    return res
