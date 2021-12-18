from django import template

from django.db.models import Count, Max
from utm.models import UTM

register = template.Library()

@register.inclusion_tag('utm/visit_overview.html', takes_context=True)
def visit_overview(context):
    """Provide a short summary of page visits.
    """
    request = context['request']
    path = request.path
    context['robots'] = UTM.objects.filter(base_url=path, ua_is_bot=True).count()
    context['humans'] = UTM.objects.filter(base_url=path, ua_is_bot=False).count()
    context['humans_unique'] = UTM.objects.filter(base_url=path, ua_is_bot=False) \
                                          .values('session_id').distinct().count()
    sources = UTM.objects.filter(base_url=path, ua_is_bot=False) \
                         .values('source').distinct()
    print(sources)
    context['sources'] = {}
    for source in sources:
        this_source = source['source']
        print('source', this_source)
        the_count = UTM.objects.filter(
            base_url=path, source=this_source, ua_is_bot=False) \
                               .values('session_id').distinct().count()
        if "" == this_source:
            # This should be doable with the |default filter in the template
            # but that's not working for me.
            this_source = "<aucun>"
        context['sources'][this_source] = the_count
    return context
