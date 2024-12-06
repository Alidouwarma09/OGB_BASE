from django import template

register = template.Library()

@register.filter
def get_item(value, index):
    """Filtre pour accéder à un élément d'une liste ou d'un dictionnaire par son index"""
    try:
        return value[index]
    except (IndexError, TypeError):
        return None
