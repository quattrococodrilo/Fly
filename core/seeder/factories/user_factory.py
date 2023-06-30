import factory
from factory.django import DjangoModelFactory
import faker

class UserFactory(DjangoModelFactory):
    class Meta:
        model = "core.User"

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")


# import faker

# fake = faker.Faker()

# class BookFactory(DjangoModelFactory):
#     class Meta:
#         model = Book

#     title = factory.LazyAttribute(lambda x: fake.sentence(nb_words=4))
#     author = factory.LazyAttribute(lambda x: fake.name())
#     publication_date = factory.LazyAttribute(lambda x: fake.date_between(start_date='-30y', end_date='today'))



# class SubcategoryFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = "api.Subcategory"

#     category = factory.SubFactory(CategoryFactory)
#     description = factory.Faker("sentence"
