from django import template

register = template.Library()


@register.filter
def pl_plural(count, forms):
    """Polish plural: {{ n|pl_plural:"artykuł,artykuły,artykułów" }}"""
    one, few, many = forms.split(',')
    count = int(count)
    if count == 1:
        return one
    if count % 10 in (2, 3, 4) and count % 100 not in (12, 13, 14):
        return few
    return many


LOCATIVE = {1: 'jednym', 2: 'dwóch', 3: 'trzech', 4: 'czterech', 5: 'pięciu',
            6: 'sześciu', 7: 'siedmiu', 8: 'ośmiu', 9: 'dziewięciu', 10: 'dziesięciu'}


@register.filter
def pl_locative(count):
    """Number as a Polish locative word: {{ 4|pl_locative }} -> "czterech" (digits above ten)"""
    return LOCATIVE.get(int(count), count)
