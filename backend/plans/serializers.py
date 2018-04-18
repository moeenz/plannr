from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated

from events.models import Plan
from utils.request import get_request_user


class PlanSerializer(serializers.Serializer):
    """Serializer for requests coming upon /plans api.
    `django-restframework does not support ModelSerializers so
    a bare serializer is need.`
    """

    start = serializers.DateTimeField(required=True)
    end = serializers.DateTimeField(required=True)
    desc = serializers.CharField(required=True)

    def create(self, validated_data):
        request_user = get_request_user(self.context.get('request'))
        if request_user:
            return Plan.objects.create(
                owner_id=request_user.id,
                start=validated_data.get('start', None),
                end=validated_data.get('end', None),
                desc=validated_data.get('desc', None)
            )
        else:
            raise NotAuthenticated
