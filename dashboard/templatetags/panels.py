from django import template


register = template.Library()


@register.inclusion_tag('panel.html')
def default_panel(heading, body, footer=None):
    return {'heading': heading,
            'body': body,
            'footer': footer}
