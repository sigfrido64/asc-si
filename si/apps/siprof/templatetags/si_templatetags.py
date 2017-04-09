# coding=utf-8
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def can_add(user, app):
    print(user)
    return user.profile.can_add(app)


@register.filter
def can_export(user, app):
    return user.profile.can_export(app)


@register.filter
def can_import(user, app):
    return user.profile.can_import(app)


@register.filter
def can_read(user, app):
    return user.profile.can_read(app)


@register.filter
def can_update(user, app):
    return user.profile.can_update(app)


@register.filter
def can_delete(user, app):
    return user.profile.can_delete(app)

