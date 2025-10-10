from typing import Any

from django import template
from django.http import HttpRequest

register = template.Library()


@register.simple_tag()
def update_query_string(request: HttpRequest, value: Any, key: str = 'page') -> str:
    """
    Adds the parameter to GET query string
    """
    params = request.GET.copy()
    params[key] = value
    return params.urlencode()


@register.filter
def create_range(value: int, start_index: int = 1) -> range:
    """
    Creates a range of numbers from 1 to value
    """
    return range(start_index, value+1)
