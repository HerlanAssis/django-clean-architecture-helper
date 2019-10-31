from django.core.cache import cache


class BaseCache:
    def __init__(self, timeout=60, version=None):
        self._timeout = timeout
        self._version = version

    def get_cache(self, key):
        return cache.get(key)

    def set_cache(self, key, instance_object):
        return cache.set(key, instance_object, self._timeout)

    def delete_cache(self, key):
        return cache.delete(key, self._version)
