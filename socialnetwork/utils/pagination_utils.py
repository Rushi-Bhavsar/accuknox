from django.conf import settings
from rest_framework.pagination import PageNumberPagination


def paginate_response(query_set, request, serializer):
    paginator = PageNumberPagination()
    paginator.page_size = settings.REST_FRAMEWORK.get('PAGE_SIZE', 20)
    paginator.page_query_param = 'page'
    p_data = paginator.paginate_queryset(queryset=query_set, request=request)
    serialized = serializer(p_data, many=True)
    resp_data = paginator.get_paginated_response(serialized.data)
    return resp_data

