from django import template

register = template.Library()


@register.inclusion_tag('ui/base_component.html', takes_context=True)
def ui_insert(context, template: str, ctx: str = "", **kwargs):
    """Insert template in other template.

    Args:
        context (RequestContext): Request context
        template (string): Path to template file
        from_ctx (str, optional): By default all request context is passed, but this can be more selective, is you specify context keys in this argument. Keys must be separated by commas. Defaults to "".

    Returns:
        dict: Template context.
    """

    _ctx: dict = {}

    if ctx:
        from_ctx_splitted = [i.strip() for i in ctx.split(',')]
        _ctx = {key: context.get(key, None) for key in from_ctx_splitted}
    else:
        _ctx = context.flatten()

    return {
        **_ctx,
        ** kwargs,
        'template': template,
    }
