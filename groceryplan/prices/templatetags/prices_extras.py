from django import template
from prices.models import PC

register = template.Library()


def production(value):
    return PC[value]

register.filter('production', production)
