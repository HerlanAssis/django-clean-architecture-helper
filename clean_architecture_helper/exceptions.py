from django.utils.translation import ugettext_lazy as _


class BaseException(Exception):
    def __init__(self, source, code, message):
        super().__init__(message)
        self._source = source
        self._code = code

    @property
    def source(self):
        return self._source

    @property
    def code(self):
        return self._code


class InvalidEntityException(BaseException):
    pass


class EntityDoesNotExistException(BaseException):

    def __init__(self):
        super().__init__(source='entity',
                         code='not_found',
                         message=_('Entidade não encontrada'))