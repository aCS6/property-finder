from django import template

register = template.Library()

def range_filter(value):
    return value[0:350] + "......"

def range_filter2(value):
    return value[0:100] + "......"

register.filter('range_filter',range_filter)
register.filter('range_filter2',range_filter2)