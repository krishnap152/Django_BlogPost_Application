import urllib.parse as parse

from django import template

register = template.Library()

@register.filter
def urlify(value):
    return parse.quote_plus(value)
