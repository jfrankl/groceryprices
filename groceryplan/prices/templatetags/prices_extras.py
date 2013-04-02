from django import template

register = template.Library()


def remove_lead_zero(value):
    num_as_string = str(value)
    return num_as_string.lstrip('0')

register.filter('remove_lead_zero', remove_lead_zero)
