# Django-Vite-Tailwind-Docker

This implementation allows you develop a Django Web Project with auto reload powered by Vite.

## Install

Clone this repo and:

`./fly build`
`./fly up`

## Fly Manager

Fly is a command line tool for managing your Django projects.

positional arguments:

- `./fly.py install`:             Install app.
- `./fly.py up`:                  Up services.
- `./fly.py down`:                Down services.
- `./fly.py d`:                   Execute docker compose commands.
- `./fly.py pip`:                 Execute pip commands
- `./fly.py manage`:              Execute Django Manager
- `./fly.py npm`:                 Execute npm
- `./fly.py mysql`:               Execute MySql
- `./fly.py psql`:                Execute PostgreSQL
- `./fly.py runserve-alone`:      Run Django server alone

## Create New App

When create a new a app with `./fly manage startapp {app_name}`, the app will be
created in apps directory, you can change this in the .env file.

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

## Tailwindcss

Tailwind CSS enables hot reloading in Django, and the classes in the forms can
be parsed by Tailwind CSS.

## TODO

1. [X] Change fly manger from Bash to Python.
2. [ ] Better documentation for **fly** manager.
3. [ ] Finish help menú.
