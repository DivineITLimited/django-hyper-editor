from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.db.models import Q, Model
import functools


class Chooser(object):
    queryset = None
    fields = None
    search_fields = None
    ordering = '-id'

    def get_queryset(self):
        return self.queryset

    def get_name(self):
        queryset = self.get_queryset()
        return '%s|%s' % queryset.model._meta.app_label, queryset.model.__name__

    def filter(self, q, queryset):
        if isinstance(self.search_fields, list):
            queries = [Q(**{"%s__icontains" % field: q}) for field in self.search_fields]
            queryset = queryset.filter(functools.reduce(lambda x, y: x | y, queries))
        return queryset

    def get_ordering(self, queryset):
        return queryset.order_by(self.ordering)

    def get_fields(self, queryset):
        if isinstance(self.fields, list):
            return queryset.values(*self.fields)
        return queryset

    def get_paginator(self, q=None, per_page=20):
        queryset = self.get_queryset()
        queryset = self.filter(q, queryset)
        queryset = self.get_ordering(queryset)
        queryset = self.get_fields(queryset)
        paginator = Paginator(queryset, per_page=per_page)
        return paginator

    def serialize(self, item):
        if isinstance(item, Model):
            return model_to_dict(item)
        else:
            return item

    def paginate(self, request, q, page=1):
        paginator = self.get_paginator(q)
        page_obj = paginator.page(page)
        result = [self.serialize(item) for item in page_obj.object_list]
        return {
            'total': paginator.count,
            'per_page': paginator.per_page,
            'current_page': page,
            'result': result,
        }