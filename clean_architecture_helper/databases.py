from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .exceptions import EntityDoesNotExistException


class BaseDatabase:
    def __init__(self, orm, entity):
        self._entity = entity
        self._orm = orm

    def __str__(self):
        app_label = self._orm._meta.app_label
        model_name = self._orm._meta.model_name
        return "{}:{}".format(app_label, model_name)

    def _create(self, **kwargs):
        return self._orm.objects.create(**kwargs)

    def create(self, **kwargs):
        return self._decode_db(self._create(**kwargs))

    def _update(self, **kwargs):
        id = kwargs.get('id')
        
        self._orm.objects.filter(pk=id).update(**kwargs)
        
        orm_instance = self._orm.objects.get(pk=id)

        return orm_instance

    def update(self, **kwargs):
        return self._decode_db(self._update(**kwargs))

    def _get(self, **kwargs):
        try:
            return self._orm.objects.get(**kwargs)
        except ObjectDoesNotExist:
            raise EntityDoesNotExistException

    def get(self, **kwargs):
        return self._decode_db(self._get(**kwargs))

    def _filter(self, **kwargs):
        if kwargs.pop('force_all', False):        
            return self._orm.objects.all()
        return self._orm.objects.actives()

    def filter(self, **kwargs):
        orm_instance = self._filter(**kwargs)

        if kwargs:
            filter = Q()
            for key, value in kwargs.items():
                filter.add(Q(**{key: value}), Q.OR)
            orm_instance = orm_instance.filter(filter)

        return self._decode_db(orm_instance, many=True)

    def _delete(self, id):
        try:
            orm_instance = self._orm.objects.get(pk=id)
            orm_instance.inactive()
            return orm_instance
        except ObjectDoesNotExist:
            raise EntityDoesNotExistException

    def delete(self, id):
        return self._decode_db(self._delete(id=id))

    def _decode_db(self, orm_instance, many=False):
        if many:
            return [self._decode_db(orm) for orm in orm_instance]
        return self._entity(
            **vars(orm_instance)
        )
