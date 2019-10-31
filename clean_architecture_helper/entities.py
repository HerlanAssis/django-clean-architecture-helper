class BaseEntity(object):
    def __init__(self, id, created_at, updated_at, deleted_at, **kwargs):
        self._id = id
        self._created_at = created_at
        self._updated_at = updated_at
        self._deleted_at = deleted_at

    @property
    def id(self):
        return self._id

    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at

    @property
    def deleted_at(self):
        return self._deleted_at

    @property
    def is_deleted(self):
        return self.deleted_at != None
