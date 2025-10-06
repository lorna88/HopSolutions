from django import template

register = template.Library()

@register.simple_tag()
def update_query_string(request, value, key='page'):
    """
    Adds the parameter to GET query string
    """
    params = request.GET.copy()
    params[key] = value
    return params.urlencode()

@register.filter
def create_range(value, start_index=1):
    """
    Creates a range of numbers from 1 to value
    """
    return range(start_index, value+1)