import graphene
from graphql_relay import from_global_id
from .types import ErrorType, ValidationErrorType


class BaseMutationOptions(graphene.types.mutation.MutationOptions):
    view_factory = None
    lookup_field = None


class BaseMutation(graphene.ClientIDMutation):
    class Meta:
        abstract = True

    errors = graphene.Field(
        ErrorType, description="May contain more than one error."
    )

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        view_factory=None,
        lookup_field=None,
        **options
    ):

        if not view_factory:
            raise Exception("view_factory is required for the Mutation")

        if not lookup_field:
            raise Exception("lookup_field is required for the Mutation")

        _meta = BaseMutationOptions(cls)
        _meta.view_factory = view_factory
        _meta.lookup_field = lookup_field

        super(BaseMutation, cls).__init_subclass_with_meta__(
            _meta=_meta,
            **options
        )


class CreateOrUpdateMutationOptions(BaseMutationOptions):
    operations = ["create", "update"]
    response_name = None


class CreateOrUpdateMutation(BaseMutation):
    class Meta:
        abstract = True

    validation_errors = graphene.List(
        ValidationErrorType, description="May contain more than one error for same field."
    )

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        operations=("create", "update"),
        response_name=None,
        view_factory=None,
        lookup_field=None,
        **options
    ):
        if "update" not in operations and "create" not in operations:
            raise Exception('operations must contain "create" and/or "update"')

        if response_name is None:
            raise Exception(
                'response_name is required for this create update mutation')

        _meta = CreateOrUpdateMutationOptions(cls)
        _meta.view_factory = view_factory
        _meta.lookup_field = lookup_field
        _meta.operations = operations
        _meta.response_name = response_name

        super(BaseMutation, cls).__init_subclass_with_meta__(
            _meta=_meta,
            **options
        )

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        operations = cls._meta.operations
        lookup_field = cls._meta.lookup_field
        view_factory = cls._meta.view_factory
        response_name = cls._meta.response_name

        try:
            input[lookup_field] = from_global_id(input[lookup_field])[1]
        except Exception:
            pass

        if "update" in operations and lookup_field in input:
            body, status, errors, validation_errors = view_factory.create().update(**input)
        elif "create" in operations:
            body, status, errors, validation_errors = view_factory.create().create(**input)
        else:
            raise Exception(
                'Invalid update operation. Input parameter "{}" required.'.format(
                    lookup_field
                )
            )

        return cls(**{response_name: body}, errors=errors, validation_errors=ValidationErrorType.from_errors(validation_errors))


class DeleteMutation(BaseMutation):
    class Meta:
        abstract = True

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        lookup_field = cls._meta.lookup_field
        view_factory = cls._meta.view_factory

        try:
            input[lookup_field] = from_global_id(input[lookup_field])[1]
        except Exception:
            pass

        if lookup_field in input:
            body, status, errors = view_factory.create().delete(
                **{lookup_field: input[lookup_field]})
        else:
            raise Exception(
                'Invalid delete operation. Input parameter "{}" required.'.format(
                    lookup_field
                )
            )

        if errors:
            return cls(ok=False, errors=errors)

        return cls(ok=True)
