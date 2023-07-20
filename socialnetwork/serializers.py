from rest_framework import serializers
from django.contrib.auth import get_user_model

from socialnetwork.models import ConnectionRequest, Connection


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'username', 'first_name', 'last_name']



class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = get_user_model()

    def to_representation(self, instance):
        data = super(CustomUserSerializer, self).to_representation(instance)
        if 'password' in data.keys():
            data.pop('password')
            data.pop('is_staff')
            data.pop('is_superuser')
            data.pop('last_login')
            data.pop('user_permissions')
            data.pop('groups')
        return data


class SearchConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'pk']
        model = get_user_model()


class ProcessRequestSerializer(serializers.Serializer):
    to_id = serializers.IntegerField(required=True)
    request_status = serializers.CharField(required=True)

    def validate_to_id(self, to_id):
        to_user = get_user_model().objects.filter(pk=to_id).first()
        if to_user:
            return to_user
        else:
            raise serializers.ValidationError('Requested customer is not present.')

    def validate_request_status(self, request_status):
        if not request_status:
            raise serializers.ValidationError("Value of request_status should be '(accept, reject)'")
        return request_status


class SendConnectionRequestSerializer(serializers.Serializer):
    to_id = serializers.IntegerField(required=True)

    def validate_to_id(self, to_id):
        to_user = get_user_model().objects.filter(pk=to_id).first()
        if to_user:
            return to_user
        else:
            raise serializers.ValidationError('Requested customer is not present.')


class PendingRequestSerializer(serializers.ModelSerializer):
    receiver_user = serializers.IntegerField(read_only=True, source='receiver_user.pk')

    class Meta:
        model = ConnectionRequest
        fields = ['receiver_user', 'status']

    def validate(self, attrs):
        if attrs.get('status') not in ('pending', 'reject'):
            raise serializers.ValidationError("Value of status should be ('pending', 'reject')")
        return attrs


class FriendsSerializer(serializers.ModelSerializer):

    customer_username = serializers.CharField(read_only=True, source='to_user.username')

    class Meta:
        model = Connection
        fields = ('to_user', 'customer_username')
