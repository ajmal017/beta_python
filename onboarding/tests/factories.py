import uuid

import factory
import factory.fuzzy
import datetime
from faker import Factory

from onboarding.models import Individual, PhoneInfo, PhonesList, IndividualName, Address

faker = Factory.create()


class PhoneInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PhoneInfo

    type = "Home"
    number = faker.phone_number()
    country = faker.country()

class PhonesListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PhonesList

    Phone = factory.SubFactory(PhoneInfoFactory)


class IndividualNameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IndividualName

    salutation = "Mr"
    first = faker.first_name_male()
    last = faker.last_name_male()

class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    street_1 = faker.street_address()
    city = faker.city()
    state = faker.state()
    country = faker.country()
    postal_code = faker.postalcode()

class IndividualFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Individual
    idx = str(uuid.uuid4())
    external_id = idx
    Name = factory.SubFactory(IndividualNameFactory)
    DOB = datetime.datetime.strptime(faker.date(), "%Y-%m-%d").date()
    CountryOfBirth = faker.country()
    Gender = "M"
    MaritalStatus = "M"
    Residence = factory.SubFactory(AddressFactory)
    Phones = factory.SubFactory(PhonesListFactory)

