from django import template

register = template.Library()

@register.filter
def length_is(value, arg):
    """Check if the length of value is equal to arg."""
    return len(value) == arg
