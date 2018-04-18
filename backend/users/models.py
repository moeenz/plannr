import uuid

from django.db.models import UUIDField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Extended user model, replacing 'id' with a uuid field
    which is going to be used in cassandra.
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
