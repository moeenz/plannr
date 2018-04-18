from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


def get_request_user(request):
    """Returns user of the context request.
    request can be retrieved by calling context.get('request') in
    a serializer create method.
    """

    if request is not None and hasattr(request, 'user'):
        try:
            return User.objects.get(username=request.user.username)
        except ObjectDoesNotExist:
            raise None
    else:
        raise ValueError('Context request has no user attribute.')
