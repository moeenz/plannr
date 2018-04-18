from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from users.serializers import UserCreationSerializer


@api_view(['POST'])
def user_register(request):
    """API view for registering new users.
    """

    serializer = UserCreationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
