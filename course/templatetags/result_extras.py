from django import template
register = template.Library()

@register.filter
def credits_display(credits):
    if(credits):
        lowerBound = credits.lower
        upperBound = credits.upper

        return str(lowerBound) if (lowerBound == upperBound - 1) else str(lowerBound) +  " - " + str(upperBound - 1)

    else:
        return ""

@register.filter
def remove_none(input):
    if(input):
        return input
    else:
        return ""