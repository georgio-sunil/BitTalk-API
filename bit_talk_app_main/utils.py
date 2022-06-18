from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomPagination(PageNumberPagination):

    def get_paginated_response(self, data):

        if not self.page.has_next():
            next = None
        else:
            next = self.page.next_page_number()

        if not self.page.has_previous():
            prev = None
        else:
            prev = self.page.previous_page_number()
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', next),
            ('previous', prev),
            ('results', data)
        ]))
