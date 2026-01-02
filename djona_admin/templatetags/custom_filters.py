from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(list, index):
    try:
        return list[index]
    except IndexError:
        return None


@register.filter
def startswith(value, arg):
    return value.startswith(arg)

def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='limit_words')
def limit_words(value, num_words):
    words = value.split()
    return ' '.join(words[:num_words])