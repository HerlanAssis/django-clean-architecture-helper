import graphene


class BaseFilter:
    def __init__(self):
        self.force_all = graphene.Boolean()
