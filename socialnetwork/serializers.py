from rest_framework import serializers
from django.contrib.auth import get_user_model


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
