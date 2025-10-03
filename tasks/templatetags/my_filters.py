from django import template

register = template.Library()

@register.simple_tag()
def update_query_string(request, value, key='page'):
    params = request.GET.copy()
    params[key] = value
    return params.urlencode()

@register.filter
def create_range(value, start_index=1):
    return range(start_index, value+1)

@register.filter
def subtract(value1, value2):
    return value1 - value2