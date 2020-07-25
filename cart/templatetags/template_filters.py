from django import template

register = template.Library()


@register.filter(name="pennies")
def pennies(number):
    value = float(number) * 100
    pennies = int(value)
    return pennies
