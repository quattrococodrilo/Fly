# Django-Vite-Tailwind-Docker

This implementation allows you develop a Django Web Project with auto reload powered by Vite.

## Install

Clone this repo and:

`./fly build`
`./fly up`

## Fly Manager

Fly is inspired in Laravel Sail, so, with this app manager you can:

- `./fly --help`: Show help.
- `./fly build`: Build image project.
- `./fly up`: Start services.
- `./fly down`: Shutdown services.
- `./fly manage`: Execute a Django command. All applications created with **startapp** will moved to apps directory.
- `./fly {npm, pnx} {command}`: Execute npm or npx command.
- `./fly mysql`: Go to MySQL cli.
- `./fly psql`: Go to PostgreSQL cli.
- `./fly exec {django, node, mysql, exec} {command}`: Execute a command in a container.

## Create New App

When create a new a app with `./fly manage startapp {app_name}`, the app will be created in apps directory.

## Seeder

To create a seeder, execute:

```bash

./fly manage make_seeder {app_name}


```

With this command you can seed your database.

```bash

./fly manage seed --seeder={app_name}.{seeder_function_name}


```

Example Factory:

```python

import factory
from factory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    class Meta:
        model = "core.User"

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")


```

Example Seeder:

```python

from .factories.user_factory import UserFactory


def user_seeder():
    UserFactory.create_batch(10)

```

Execute seeder:


```bash

./fly manage seed --seeder=core.user_seeder


```


## TODO

1. [ ] Change fly manger from Bash to Python.
2. [ ] Better documentation for **fly** manager.
3. [ ] Finish help menú.
