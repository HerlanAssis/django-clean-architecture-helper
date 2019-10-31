from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    '''
    Base serializer
    '''
    id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)
