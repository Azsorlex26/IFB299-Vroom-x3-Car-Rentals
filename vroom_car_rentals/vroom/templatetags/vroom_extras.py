from django import template

register = template.Library()

# Customer Django template filter for indexing an array with a variable
@register.filter
def return_item(l, i):
    try:
        return l[i]
    except:
        return None
