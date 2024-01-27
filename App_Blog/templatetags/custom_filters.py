from django import template

register = template.Library()

def content_range_filter(value):
    return value[0:500] + '...'

register.filter('content_range_filter', content_range_filter)

def card_content_range_filter(value):
    return value[0:250] + '...'

register.filter('card_content_range_filter', card_content_range_filter) 