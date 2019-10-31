from django.utils.translation import ugettext_lazy as _
from .exceptions import EntityDoesNotExistException


class BasePresentation:

    def __init__(self, serializer, operations):
        create = operations.get('create')
        get = operations.get('get')
        update = operations.get('update')
        delete = operations.get('delete')
        all = operations.get('all')

        self._create = create
        self._get = get
        self._update = update
        self._delete = delete
        self._all = all

        self._serializer = serializer

    def get(self, id):
        body = {}
        status = 200
        errors = []

        try:
            obj = self._get \
                .set_params(id=id) \
                .execute()
        except EntityDoesNotExistException:
            errors.append(_('Nenhum resultado encontrado!'))
            status = 500
        else:
            body = self._serializer(obj).data

        return body, status, errors

    def create(self, **kwargs):
        body = {}
        status = 200
        errors = []
        validation_errors = {}

        obj = self._serializer(data=kwargs)

        if not obj.is_valid():
            errors.append(_("Entrada de dados inválidos!"))
            status = 500
            validation_errors = obj.errors
            return body, status, errors, validation_errors

        obj = self._create \
            .set_params(**kwargs) \
            .execute()

        body = self._serializer(obj).data
        return body, status, errors, validation_errors

    def update(self, **kwargs):
        body = {}
        status = 200
        errors = []
        validation_errors = {}

        obj = self._serializer(data=kwargs)

        if not obj.is_valid():
            errors.append(_("Entrada de dados inválidos!"))
            status = 409
            validation_errors = obj.errors
            return body, status, errors, validation_errors

        obj = self._update \
            .set_params(**kwargs) \
            .execute()

        body = self._serializer(obj).data

        return body, status, errors, validation_errors

    def delete(self, id):
        body = {}
        status = 200
        errors = []

        try:
            obj = self._delete \
                .set_params(id=id) \
                .execute()
        except EntityDoesNotExistException:
            errors.append(_('Nenhum resultado encontrado!'))
            status = 500
        else:
            body = self._serializer(obj).data

        return body, status, errors

    def all(self, force_all=False, **kwargs):
        body = {}
        status = 200
        errors = []

        try:
            obj = self._all \
                .set_params(force_all=force_all, **kwargs) \
                .execute()
        except Exception:
            errors.append(_("Ocorreu um erro ao obter os resultados"))
            status = 500
        else:
            body = self._serializer(obj, many=True).data

        return body, status, errors
