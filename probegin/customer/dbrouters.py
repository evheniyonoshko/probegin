import os

from probegin import settings
from customer.models import ReplicaCustomer, ReplicaCustomerDiscount


class PrimaryReplicaRouter:
    def is_replica_model(self, model):
        return model in [
            ReplicaCustomer,
            ReplicaCustomerDiscount,
            ReplicaCustomer._meta.model_name,
            ReplicaCustomerDiscount._meta.model_name
        ]

    def db_for_read(self, model, **hints):
        """
        Reads go to replica db if model from replica db.
        """
        return 'replica' if self.is_replica_model(model) else 'default'

    def db_for_write(self, model, **hints):
        """
        Writes go to replica db if model from replica db.
        """
        return 'default' if not self.is_replica_model(model) else 'replica'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the default/replica pool.
        """
        db_list = ('default', 'replica')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Only defaut database
        """
        if self.is_replica_model(model_name):
            if db == 'replica':
                return True
        else:
            if db == 'default':
                return True
        return False
