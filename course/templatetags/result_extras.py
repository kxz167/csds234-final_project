from django import template
register = template.Library()

@register.filter
def credits_display(credits):
    lowerBound = credits.lower
    upperBound = credits.upper
    # return if (lowerBound == upperBound - 1)
    if(lowerBound == upperBound - 1):
        return lowerBound
    else:
        return str(lowerBound) +  " - " + str(upperBound - 1)