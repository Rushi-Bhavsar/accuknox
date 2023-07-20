from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import CustomUserSerializer, SearchConnectionSerializer, PendingRequestSerializer, FriendsSerializer,\
    ProcessRequestSerializer, SendConnectionRequestSerializer, SignUpSerializer
from .utils.core_utils import check_request_allowed, check_connection_request_already_sent, check_valid_email, \
    already_connected, send_new_connection_request
from .utils.decorator_utils import CatchException
from .utils.pagination_utils import paginate_response
from .models import ConnectionRequest, Connection
from django.utils.decorators import method_decorator


@method_decorator(CatchException, name='post')
class SignUp(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=self.request.data)
        if serializer.is_valid() is False:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_model = get_user_model()
        customer = user_model.objects.create_user(**serializer.validated_data)
        resp_data = {'code': 100, 'msg': 'New User Created successfully', 'customer_id': customer.pk}
        return Response(status=status.HTTP_201_CREATED, data=resp_data)


@method_decorator(CatchException, name='list')
@method_decorator(CatchException, name='retrieve')
class CustomerDetails(ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer

    def get_queryset(self, **kwargs):
        data = self.queryset.get(pk=kwargs['pk'])
        return data

    def retrieve(self, request, *args, **kwargs):
        query_data = self.get_queryset(**kwargs)
        if request.user.pk != query_data.pk:
            return Response({'Customer': [], 'msg': 'You are not authorized to make this request'},
                            status=status.HTTP_401_UNAUTHORIZED)
        if query_data:
            serializer_data = self.get_serializer(query_data)
            msg = 'Customer Detail found.'
            resp_data = {'Customer': serializer_data.data, 'msg': msg}
            return Response(data=resp_data, status=status.HTTP_200_OK)
        else:
            msg = 'Details not present.'
            resp_data = {'Customer': [], 'msg': msg}
            return Response(data=resp_data, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not self.request.user.is_superuser or self.request.user.is_staff:
            return Response({'Customer': [], 'msg': 'You are not authorized to make this request'},
                            status=status.HTTP_401_UNAUTHORIZED)
        msg = 'All user list'
        resp_data = paginate_response(self.queryset, request, self.serializer_class)
        data_content = {'code': 100, 'msg': msg, 'total_count': resp_data.data['count'],
                        'page_count': len(resp_data.data['results']), 'next': resp_data.data['next'],
                        'previous': resp_data.data['previous'], 'result': resp_data.data['results']}
        return Response(data=data_content, status=status.HTTP_200_OK)


@method_decorator(CatchException, name='list')
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
        return Response(data=data_content, status=status.HTTP_200_OK)


class SendConnectionRequest(APIView):

    def post(self, request):
        from_user = self.request.user
        serializer = SendConnectionRequestSerializer(data=request.data)
        if serializer.is_valid() is False:
            return Response(data=serializer.errors, status=200)
        to_user = serializer.validated_data.get('to_id')

        # User can not send more than three connection request within 60 seconds.
        connection_count = check_request_allowed(from_user)
        if connection_count >= 3:
            msg = 'Can not send more than 3 new connection request within 1 min.'
            resp_data = {'msg': msg}
            return Response(status=status.HTTP_400_BAD_REQUEST, data=resp_data)

        # Check if connection is already present.
        connection_present = already_connected(from_user, to_user)
        if connection_present:
            msg = 'Connection is already present. Can not send new request.'
            resp_data = {'msg': msg}
            return Response(status=status.HTTP_400_BAD_REQUEST, data=resp_data)

        # Check if request is already sent.
        connection_already_send = check_connection_request_already_sent(from_user, to_user)
        if connection_already_send:
            msg = 'Connection request already sent.'
            resp_data = {'msg': msg}
            return Response(status=status.HTTP_400_BAD_REQUEST, data=resp_data)

        # Create new connection request.
        msg = send_new_connection_request(from_user, to_user)
        resp_data = {'msg': msg}
        return Response(status=status.HTTP_201_CREATED, data=resp_data)


@method_decorator(CatchException, name='post')
class ProcessRequest(APIView):
    def post(self, request):
        from_user = self.request.user
        serializer = ProcessRequestSerializer(data=request.data)
        if serializer.is_valid() is False:
            return Response(data=serializer.errors, status=200)
        request_status = serializer.validated_data.get('request_status')
        to_user = serializer.validated_data.get('to_id')
        query_data = ConnectionRequest.objects.filter(sender_user=from_user, receiver_user=to_user, status='pending').first()
        if query_data:
            query_data.status = request_status
            query_data.save()
            if query_data.status == 'accept':
                a = Connection(from_user=from_user, to_user=to_user, description='New Connection Added.',
                               connection_date=timezone.now().date())
                a.save()
                msg = 'Connection added.'
            else:
                msg = 'Connection Rejected'
        else:
            msg = f"No Connection request found from '{from_user}' to {to_user}"
        return Response(data={'msg': msg}, status=status.HTTP_200_OK)


@method_decorator(CatchException, name='list')
class PendingRequest(ReadOnlyModelViewSet):
    queryset = ConnectionRequest.objects.all()
    serializer_class = PendingRequestSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.query_params)
        if serializer.is_valid() is False:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        process_status = serializer.validated_data.get('status')
        query_data = self.queryset.filter(sender_user=request.user, status=process_status)
        if query_data:
            resp_data = paginate_response(query_data, request, self.serializer_class)
            msg = 'Requested Details found.'
            data_content = {'code': 100, 'msg': msg, 'total_count': resp_data.data['count'],
                            'page_count': len(resp_data.data['results']), 'next': resp_data.data['next'],
                            'previous': resp_data.data['previous'], 'result': resp_data.data['results']}
            status_code = status.HTTP_200_OK
        else:
            msg = 'Requested Details not found.'
            data_content = {'msg': msg}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(status=status_code, data=data_content)


@method_decorator(CatchException, name='list')
class FriendsList(ReadOnlyModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = FriendsSerializer

    def list(self, request, *args, **kwargs):
        query_data = self.queryset.filter(from_user=request.user)
        if query_data:
            resp_data = paginate_response(query_data, request, self.serializer_class)
            msg = 'Details found.'
            data_content = {'code': 100, 'msg': msg, 'total_count': resp_data.data['count'],
                            'page_count': len(resp_data.data['results']), 'next': resp_data.data['next'],
                            'previous': resp_data.data['previous'], 'result': resp_data.data['results']}
            status_code = status.HTTP_200_OK
        else:
            msg = 'Details not found.'
            data_content = {'msg': msg}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(status=status_code, data=data_content)
