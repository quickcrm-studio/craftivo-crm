from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Add CSS classes to a form field.
    Usage: {{ form.field|add_class:"form-control" }}
    """
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='replace')
def replace(value, arg):
    """
    Replace all instances of arg in the given value.
    Usage: {{ value|replace:"_:" " }}
    """
    old, new = arg.split(":", 1) if ":" in arg else (arg, " ")
    return value.replace(old, new) 