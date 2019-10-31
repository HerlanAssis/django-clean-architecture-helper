import graphene
from graphene import Int


class TotalItemsConnection(graphene.relay.Connection):
    class Meta:
        abstract = True

    total = Int()

    def resolve_total(self, info, **kwargs):
        return len(self.iterable)


class BaseConnectionField(graphene.relay.ConnectionField):
    def __init__(self, type, *args, **kwargs):

        filters = type._meta.node._meta.filter_class
        if filters is not None:
            for key, value in vars(filters()).items():
                kwargs.setdefault(key, value)

        super(BaseConnectionField, self).__init__(type, *args, **kwargs)
