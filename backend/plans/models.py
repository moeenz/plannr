import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel


class Plan(DjangoCassandraModel):
    """Data model to store plan objects. Each plans
    will be owned by someone, containing a start/end datetime
    and a description.
    """

    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    owner_id = columns.UUID(required=True)
    start = columns.DateTime(required=True)
    end = columns.DateTime(required=True)
    desc = columns.Text(required=True)


    def __str__(self):
        return 'Plan {}'.format(self.desc)
