from django import template
register = template.Library()


@register.filter(name="clicked")
def clicked(value):
    if value==1:
        return "blue"
    else:
        return ""


@register.filter
def index(indexable, i):
    return indexable[i]
