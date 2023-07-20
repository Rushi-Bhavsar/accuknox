import logging

from rest_framework.response import Response

logger = logging.getLogger(__name__)


class CatchException:

    def __init__(self, function_view):
        self.view = function_view

    def __call__(self, request, **kwargs):
        try:
            result = self.view(request, **kwargs)
            return result
        except Exception as e:
            logger.exception(f"Error occurred while processing")
            data_context = {'code': 101, 'msg': 'System Error occurred.', 'results': []}
            return Response(data=data_context, status=400)
