import factory
from django.contrib.auth import models as auth_models
from datetime import datetime

from test_app import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = auth_models.User
        django_get_or_create = ('email',)

    username = factory.Sequence(lambda n: u"jonddue%03d" % n)
    email = factory.Sequence(lambda n: u"jonddue%03d@contentools.com" % n)
    password = factory.PostGenerationMethodCall('set_password', '123456')
    first_name = factory.Sequence(lambda n: u"John %03d" % n)
    last_name = "Due"
    is_staff = False
    is_active = True


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Project

    name = factory.Sequence(lambda n: u"Project %03d" % n)
