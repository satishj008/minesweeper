from django import template
register = template.Library()


@register.filter(name="clicked")
def clicked(value):
    if value==1:
        return "#A18FA2"
    else:
        return ""


@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter(name="flagshow")
def flagshow(value):
    if value==10:
        return "fa fa-bomb"
    else:
        return value


@register.filter(name="show")
def show(value):
    if value==10:
        return ""
    else:
        return value



@register.filter(name="customcolor")
def customcolor(value):
    if value==10:
        return "red"
    elif value==1:
        return "blue"
    elif value==2:
        return "green"
    elif value==3:
        return "red"
    else:
        return value


