from django import template

register = template.Library()


@register.simple_tag(name='get_proper_name')
def get_proper_name(name=""):
    if '-' in name:
        name = name.rsplit('-')[0]
    return name

@register.simple_tag(name='get_proper_name2')
def get_proper_name2(name=""):
    if '-' in name:
        name = name.replace("-", " ")
    return name

@register.simple_tag(name='get_from_list')
def get_from_list(list, number):
    return list[number]


@register.simple_tag(name='get_type_color')
def get_type_color(type=""):

    color_dict = {
        'normal': '#A8A77A',
        'fire': '#EE8130',
        'water': '#6390F0',
        'electric': '#F7D02C',
        'grass': '#7AC74C',
        'ice': '#96D9D6',
        'fighting': '#C22E28',
        'poison': '#A33EA1',
        'ground': '#E2BF65',
        'flying': '#A98FF3',
        'psychic': '#F95587',
        'bug': '#A6B91A',
        'rock': '#B6A136',
        'ghost': '#735797',
        'dragon': '#6F35FC',
        'dark': '#705746',
        'steel': '#B7B7CE',
        'fairy': '#D685AD'
    }

    try:
        color = color_dict[type]
    except:
        color = '#343a40'


    return color
