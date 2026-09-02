from django import template

register = template.Library()

@register.filter(name='currency')
def currency(price):
    try:
        return '{:.2f}'.format(float(price)) + ' $'
    except (ValueError, TypeError):
        return price