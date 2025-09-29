from django import template
from django.contrib.admin.templatetags.admin_list import result_headers, result_hidden_fields, items_for_result, \
    ResultList
from django.contrib.admin.templatetags.base import InclusionAdminNode

register = template.Library()

def results(cl):
    if cl.formset:
        for res, form in zip(cl.result_list, cl.formset.forms):
            yield (res, ResultList(form, items_for_result(cl, res, form)))
    else:
        for res in cl.result_list:
            yield (res, ResultList(None, items_for_result(cl, res, None)))

def result_list(cl):
    """
    Display the headers and data list together.
    """
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    return {
        'cl': cl,
        'result_hidden_fields': list(result_hidden_fields(cl)),
        'result_headers': headers,
        'num_sorted_fields': num_sorted_fields,
        'results': list(results(cl)),
        'url_object_change': "admin:%s_%s_change" % (cl.opts.app_label, cl.opts.model_name),
    }


@register.tag(name='result_list_ext')
def result_list_tag(parser, token):
    return InclusionAdminNode(
        parser, token,
        func=result_list,
        template_name='change_list_results.html',
        takes_context=False,
    )