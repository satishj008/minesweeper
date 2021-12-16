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


@register.filter(name="flagshow")
def flagshow(value):
    if value==10:
        return "B"
    else:
        return value


@register.filter(name="customcolor")
def customcolor(value):
    if value==10:
        return "red"
    else:
        return ""
