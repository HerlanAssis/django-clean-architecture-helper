import graphene
from graphene.types.objecttype import ObjectTypeOptions
from ..utils import camelize
from .settings import graphene_settings

ErrorType = graphene.List(graphene.NonNull(graphene.String), required=True)


class ValidationErrorType(graphene.ObjectType):
    field = graphene.String(required=True)
    messages = graphene.List(graphene.NonNull(graphene.String), required=True)

    @classmethod
    def from_errors(cls, errors):
        data = camelize(
            errors) if graphene_settings.CAMELCASE_ERRORS else errors
        return [cls(field=key, messages=value) for key, value in data.items()]


class BaseObjectTypeOptions(ObjectTypeOptions):
    view_factory = None
    filter_class = None


class BaseType(graphene.ObjectType):
    created_at = graphene.String()
    updated_at = graphene.String()
    deleted_at = graphene.String()
    is_deleted = graphene.Boolean()

    @classmethod
    def __init_subclass_with_meta__(
            cls,
            interfaces=(),
            possible_types=(),
            default_resolver=None,
            view_factory=None,
            filter_class=None,
            _meta=None,
            **options
    ):
        if not _meta:
            _meta = BaseObjectTypeOptions(cls)

        _meta.view_factory = view_factory
        _meta.filter_class = filter_class

        super(BaseType, cls).__init_subclass_with_meta__(
            _meta=_meta, interfaces=interfaces, **options
        )

    @classmethod
    def get_node(cls, info, id):
        body, status, errors = cls._meta.view_factory.create().get(id)
        return body
