DEFAULT_DB_APPS = (
    'auth',
    'admin',
    'contenttypes',
    'sessions'
)

class DBRouter:
    """Database router for selecting between 'default' and
    'cassandra' database. Django auth apps don't play well
    with django-cassandra-engine implementation of models. 
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label in DEFAULT_DB_APPS:
            return 'default'
        else:
            return 'cassandra'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in DEFAULT_DB_APPS:
            return 'default'
        else:
            return 'cassandra'

    def allow_relation(self, obj1, obj2, **hints):
            return True

    def allow_syncdb(self, db, model):
        if model._meta.app_label in DEFAULT_DB_APPS:
            return db == 'default'
        return False
