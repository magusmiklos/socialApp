
import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()  # This is necessary to register custom filters

@register.filter
def highlight_search(text, search_query):
    if not search_query:
        return text
    pattern = re.escape(search_query)
    highlighted = re.sub(
        pattern,
        f'<span class="spin-rainbow">{search_query}</span>',
        text,
        flags=re.IGNORECASE
    )
    return mark_safe(highlighted)
