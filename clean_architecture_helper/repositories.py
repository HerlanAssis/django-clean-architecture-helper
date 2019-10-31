
class BaseRepo:
    def __init__(self, database, cache=None):
        self._database = database
        self._cache = cache

    def _get_cache_key(self, id):
        return '{}:{}'.format(self._database, id)

    def create(self, **kwargs):
        return self._database.create(**kwargs)

    def get(self, **kwargs):
        id = kwargs.get('id')
        key = self._get_cache_key(id)

        obj = self._cache.get_cache(key)

        if obj is None:
            obj = self._database.get(**kwargs)
            self._cache.set_cache(key, obj)

        return obj

    def all(self, force_all, **kwargs):
        return self._database.all(force_all=force_all, **kwargs)

    def update(self, **kwargs):
        return self._database.update(**kwargs)

    def delete(self, id):
        return self._database.delete(id=id)
