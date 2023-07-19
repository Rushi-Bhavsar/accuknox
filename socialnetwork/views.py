import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_409_CONFLICT, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import CustomUserSerializer, SearchConnectionSerializer
from .utils.pagination_utils import paginate_response


class SignUp(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        customer_email = request.data.get('email')
        customer_password = request.data.get('password')
        customer_username = request.data.get('username')
        user_model = get_user_model()
        try:
            customer = user_model.objects.get(email=customer_email)
            resp_data = {'code': 100, 'msg': f"Customer already present for mention email '{customer_email}'"}
            status_code = HTTP_409_CONFLICT
        except user_model.DoesNotExist:
            customer = user_model.objects.create_user(email=customer_email, password=customer_password,
                                                      username=customer_username, is_active=True)
            resp_data = {'code': 100, 'msg': 'New User Created successfully', 'customer_id': customer.pk}
            status_code = HTTP_201_CREATED
        return Response(status=status_code, data=resp_data)


class CustomerDetails(ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer

    def get_queryset(self, **kwargs):
        data = self.queryset.get(pk=kwargs['pk'])
        return data

    def retrieve(self, request, *args, **kwargs):
        query_data = self.get_queryset(**kwargs)
        if request.user.pk != query_data.pk:
            return Response({'Customer': [], 'msg': 'You are not authorized to make this request'}, status=HTTP_401_UNAUTHORIZED)
        if query_data:
            serializer_data = self.get_serializer(query_data)
            msg = 'Customer Detail found.'
            resp_data = {'Customer': serializer_data.data, 'msg': msg}
            return Response(data=resp_data, status=HTTP_200_OK)
        else:
            msg = 'Details not present.'
            resp_data = {'Customer': [], 'msg': msg}
            return Response(data=resp_data, status=HTTP_204_NO_CONTENT)


def check_valid_email(search_field):
    pattern = r'^[\w\.]+@[\w\.]+\.(com|in)$'
    return re.match(pattern, search_field) is not None


class SearchConnection(ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = SearchConnectionSerializer

    def list(self, request, *args, **kwargs):

        search_field = self.request.query_params.get('search_name')
        request_user = request.user
        if not search_field:
            query_data = self.queryset.exclude(pk=request_user.pk).exclude(is_staff=True, is_superuser=True)
        else:
            if check_valid_email(search_field):
                query_data = self.queryset.filter(email=search_field)
            else:
                query_data = self.queryset.filter(first_name__contains=search_field)
        resp_data = paginate_response(query_data, request, self.serializer_class)
        msg = 'Search Details'
        data_content = {'code': 100, 'msg': msg, 'total_count': resp_data.data['count'],
                        'page_count': len(resp_data.data['results']), 'next': resp_data.data['next'],
                        'previous': resp_data.data['previous'], 'result': resp_data.data['results']}
        return Response(data=data_content, status=HTTP_200_OK)
