# Django Clean Architecture Helper

<!--- Alguns exemplos. Veja https://shields.io para outros escudos customizavéis. Convém incluir dependências, status do projeto e informações da licença aqui --->
![GitHub repo size](https://img.shields.io/github/repo-size/herlanassis/django-clean-architecture-helper)
![GitHub contributors](https://img.shields.io/github/contributors/herlanassis/django-clean-architecture-helper)
![GitHub stars](https://img.shields.io/github/stars/herlanassis/django-clean-architecture-helper?style=social)
![GitHub forks](https://img.shields.io/github/forks/herlanassis/django-clean-architecture-helper?style=social)
![GitHub issues](https://img.shields.io/github/issues-raw/herlanassis/django-clean-architecture-helper?style=social)
![Twitter Follow](https://img.shields.io/twitter/follow/herlanassis?style=social)

Django Clean Architecture Helper é uma `aplicação` que permite que os `desenvolvedores Django` criem `aplicações escaláveis`.

Motivação para a construção do aplicativo:
* [The clean architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
* [Django clean architecture](http://jordifierro.com/django-clean-architecture)

Obs: Para o melhor entendimento desse projeto, recomendo fortemente a leitura dos artigos acima.

Vantagens na utilização desta aplicação:
* Exclusão lógica no modelos;
* Baixo acoplamento e alta coesão de cada camada;
* CRUD simples já implementado;

## Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:
<!--- Estes são apenas exemplos de requisitos. Adicione, duplique ou remova conforme necessário --->
* Você instalou o `python 3`?;
* Você instalou uma compatível do `virtualenv`?;
* Você instalou a compatível do `virtualenvwrapper`?;
* Você instalou o `Django 3.x`?;

## Instalando Django Clean Architecture Helper

Para instalar o Django Clean Architecture Helper, siga estes passos:

1. Adicione a dependência no seu arquivo requirements.txt:
```text
git+git://github.com/herlanassis/django-clean-architecture-helper.git@master#egg=v0.3
```
1. Instale as dependências:
```shell script
pip install -r requirements.txt
```

## Utilizando Django Clean Architecture Helper

Para usar o Django Clean Architecture Helper, siga estes passos:

```python
INSTALLED_APPS = [
   ...
   django_clean_architecture_helper,
]
```

### Passos
A seguir será mostrado um exemplo de como utilizar a aplicação para estruturar o seu projeto.
Para este exemplo utilizaremos uma aplicação chamada `Post`.

#### 1º Passo: Modelagem de dados
No arquivo `models.py` insira:
```python
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_clean_architecture_helper.models import BaseModel


class ORMPost(BaseModel):
    class Meta:
        verbose_name: _("Post")
        verbose_name_plural: _("Posts")

    title = models.CharField(
        verbose_name=_("Título"),
        max_length=64
    )
    content = models.TextField(
        verbose_name=_("Conteúdo")
    )

    def __str__(self):
        return self.title
```
A herança do classe `BaseModel` permite que o modelo tenha a funcionalidade de exclusão lógica.

### 2º Passo: Criação da entidada modelada no banco
É importante utilizar uma `entity` como como retorno para não entregar o objeto ORM como resposta a
solicitação de uma camada mais exterior e viole a regra de acesso a camadas. 
```python
from django_clean_architecture_helper.entities import BaseEntity


class Post(BaseEntity):
    def __init__(self, title, content, **kwargs):
        if kwargs:
            super().__init__(**kwargs)

        self._title = title
        self._content = content

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content
```

### 3º Passo: Criação da camada de acesso aos dados
Crie o arquivo `databases.py` e adicione o seguinte código:
```python
from django_clean_architecture_helper.databases import BaseDatabase
from .models import ORMPost
from .entities import Post


class PostDatabaseRepo(BaseDatabase):
    def __init__(self):
        super().__init__(ORMPost, Post)
```
Por padrão o `PostDatabase` vai ter acesso aos métodos existentes no arquivo `BaseDatabaseRepo` (CRUD básico para um modelo).

### 4º Passo: Crie uma camada de cache de dados
Crie o arquivo `caches.py` com o conteúdo:
```python
from django_clean_architecture_helper.caches import BaseCache


class PostCacheRepo(BaseCache):
    pass
```
Para este exemplo não é necessário implementar nenhum método na camada de cache, o `BaseCache` vai atender as necessidades.

### 5º Passo: Crie um repositório para consulta dos dados
Crie o arquivo `repositories.py` com o código:
```python
from django_clean_architecture_helper.repositories import BaseRepo

class PostEntityRepo(BaseRepo):
    def __init__(self, db_repo, cache_repo):
        super().__init__(db_repo, cache_repo)
```
Por padrão o `PostEntityRepo` vai ter acesso aos métodos existentes no arquivo `BaseRepo` (CRUD básico).

### 6º Passo: Crie uma camada de interações (Casos de uso)
Crie um arquivo chamado `interactors.py` e crie os seguintes casos de uso:
```python
from django_clean_architecture_helper.interactors import BaseGetInteractor, BaseDeleteInteractor, BaseCreateInteractor, BaseAllInteractor, BaseUpdateInteractor


class GetPostInteractor(BaseGetInteractor):
    pass


class CreatePostInteractor(BaseCreateInteractor):
    pass


class UpdatePostInteractor(BaseUpdateInteractor):
    pass


class FilterPostsInteractor(BaseFilterInteractor):
    pass


class DeletePostsInteractor(BaseDeleteInteractor):
    pass
```

### 7º Passo: Crie uma camada de apresentação
Crie um arquivo chamado `presentations.py` e adicione o código:
```python
from django_clean_architecture_helper.presentations import BasePresentation
from .serializers import PostSerializer


class PostPresentation(BasePresentation):
    def __init__(self, operations):
        super().__init__(serializer=PostSerializer, operations=operations)

```
Repare que para este exemplo não é necessário criar nenhum método adicional,
os métodos referente ao CRUD já foram implementados. Mas, é necessário criar
um serializer para conseguir apresentar os dados ao seu solicitante.
```python
from rest_framework import serializers
from django_clean_architecture_helper.serializers import BaseSerializer


class PostSerializer(BaseSerializer):
    '''
    Post serializer
    '''
    title = serializers.CharField(required=True)
    content = serializers.CharField(required=False)

```

### 8º Passo: Crie uma fábrica
Para conectar todos os elementos anteriores é necessário criar
uma fábríca de dependências e injetar nas instâncias que desejar obter.

```python
from .repositories import PostEntityRepo
from .databases import PostDatabaseRepo
from .caches import PostCacheRepo
from .interactors import GetPostInteractor, CreatePostInteractor, UpdatePostInteractor, FilterPostsInteractor, DeletePostsInteractor
from .presentation import PostPresentation

# Repositories
class PostDatabaseRepoFactory:

    @staticmethod
    def get():
        return PostDatabaseRepo()


class PostCacheRepoFactory:

    @staticmethod
    def get():
        return PostCacheRepo()


# Entities
class PostEntityRepoFactory:
    @staticmethod
    def get():
        db_repo = PostDatabaseRepoFactory.get()
        cache_repo = PostCacheRepoFactory.get()
        return PostEntityRepo(db_repo, cache_repo)


# Interactors (User Cases)
class GetPostInteractorFactory:

    @staticmethod
    def get():
        post_repo = PostEntityRepoFactory.get()
        return GetPostInteractor(post_repo)


class CreatePostInteractorFactory:

    @staticmethod
    def get():
        post_repo = PostEntityRepoFactory.get()
        return CreatePostInteractor(post_repo)


class UpdatePostInteractorFactory:

    @staticmethod
    def get():
        post_repo = PostEntityRepoFactory.get()
        return UpdatePostInteractor(post_repo)


class DeletePostInteractorFactory:

    @staticmethod
    def get():
        post_repo = PostEntityRepoFactory.get()
        return DeletePostsInteractor(post_repo)


class FilterPostsInteractorFactory:

    @staticmethod
    def get():
        post_repo = PostEntityRepoFactory.get()
        return FilterPostsInteractor(post_repo)

# Presentations
class PostPresentationFactory:

    @staticmethod
    def create():
        create_post_interactor = CreatePostInteractorFactory.get()
        get_post_interactor = GetPostInteractorFactory.get()
        update_post_interactor = UpdatePostInteractorFactory.get()
        delete_post_interactor = DeletePostInteractorFactory.get()
        filter_posts_interactor = FilterPostsInteractorFactory.get()

        operations = {
            'create': create_post_interactor,
            'get': get_post_interactor,
            'update': update_post_interactor,
            'delete': delete_post_interactor,
            'filter': filter_posts_interactor,
        }

        return PostPresentation(operations=operations)
```
Repare que cada fábrica gera os seus objetos e passa para eles uma "injeção de dependências".

#### Observações
Neste ponto já temos o necessário para retornar uma resposta a uma `request` de um usuário,
para exemplificar isso, vamos continuar o processo utilizando o `graphql` como a
camada de iteração entre as requisições e a nossa apresentação. Vale lembrar que
também é possível utilizar `endpoints rest` para isso.

### 9º Passo: Exemplo com Graphql (Opcional)
* [https://github.com/HerlanAssis/django-clean-architecture-helper-gql-extension](https://github.com/HerlanAssis/django-clean-architecture-helper-gql-extension)

## TODO

As próximas ações para o projeto são:

* [x] ~~Escrever README~~
* [ ] Escrever Documentação
* [ ] Escrever Testes

## Contribuindo para Django Clean Architecture Helper

Para contribuir com Django Clean Architecture Helper, siga estes passos:

1. Fork esse repositório.
2. Crie uma branch: `git checkout -b <branch_name>`.
3. Faça suas mudanças e comite para: `git commit -m '<commit_message>'`
4. Push para a branch de origem: `git push origin Django Clean Architecture Helper/<location>`
5. crie um pull request.

Como alternativa, consulte a documentação do GitHub em [criando uma pull request](https://help.github.com/pt/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contribuidores

Agradeço às seguintes pessoas que contribuíram para este projeto:

* [@herlanassis](https://github.com/herlanassis)

## Contato

Se você quiser entrar em contato comigo, entre em contato com herlanassis@gmail.com.

## License
<!--- Se você não tiver certeza de qual licença aberta usar, consulte https://choosealicense.com --->
Este projeto usa a seguinte licença: [Apache 2.0](https://spdx.org/licenses/Apache-2.0.html).
