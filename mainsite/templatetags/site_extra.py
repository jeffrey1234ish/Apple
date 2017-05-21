#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
from django import template
import re
from django.conf import settings

register = template.Library()

@register.filter
def random_number(length=3):
    """
    Create a random integer with given length.
    For a length of 3 it will be between 100 and 999.
    For a length of 4 it will be between 1000 and 9999.
    """
    return randint(10**(length-1), (10**(length)-1))

numeric_test = re.compile("^\d+$")

def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID

def color_to_chinese(color):
    if color == "Wooden_Black":
        return u"黑橡"
    elif color == "Wooden_White":
        return u"白木紋"
    elif color == "Maple":
        return u"楓木"
    elif color == "Light_Walnut":
        return u"淺胡桃"
    elif color == "Oak":
        return u"橡木"
    elif color == "Red_Cherry":
        return u"紅櫻桃"
    elif color == "Glossy_White":
        return u"白亮光"


register.filter('getattribute', getattribute)
register.filter('color_to_chinese', color_to_chinese)
