from django import template
register = template.Library()


@register.filter(name="clicked")

def clicked(value,**args):
    print("from filter",value)
    print(args)
    return "blue"
