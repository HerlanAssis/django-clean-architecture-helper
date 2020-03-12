
class BaseGetInteractor:
    def __init__(self, repo):
        self.repo = repo

    def set_params(self, id):
        self.id = id
        return self

    def execute(self):
        return self.repo.get(id=self.id)


class BaseCreateInteractor:
    def __init__(self, repo):
        self.repo = repo

    def set_params(self, **kwargs):
        self.kwargs = kwargs
        return self

    def execute(self):
        return self.repo.create(**self.kwargs)


class BaseUpdateInteractor:
    def __init__(self, repo):
        self.repo = repo

    def set_params(self, **kwargs):
        self.kwargs = kwargs
        return self

    def execute(self):
        return self.repo.update(**self.kwargs)


class BaseFilterInteractor:
    def __init__(self, repo):
        self.repo = repo

    def set_params(self, **kwargs):        
        self.kwargs = kwargs
        return self

    def execute(self):
        return self.repo.all(**self.kwargs)


class BaseDeleteInteractor:
    def __init__(self, repo):
        self.repo = repo

    def set_params(self, id):
        self.id = id
        return self

    def execute(self):
        return self.repo.delete(id=self.id)
