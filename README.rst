===============
django-pieguard
===============

django-pieguard is a simple authorization class for tastypie that uses
django-guardian to handle object permissions.

Requirements
------------

* Python 2.7+
* Django_ 1.7
* django-guardian_ 1.2.4
* tastypie_ 0.12.1

Not tested in other versions yet.

Quickstart
----------

Install django-pieguard:

    .. code-block:: shell

        pip install django-pieguard

Then use it in a tastypie project:

    .. code-block:: python

        from pieguard.authorization import GuardianAuthorization
        from tastypie.resources import Resource
        from django.db import models

        class MyModel(models.Model):
            class Meta:
                permissions = (
                    ('view_mymodel', 'View my model'),
                )

        class MyResource(ModelResource):
            class Meta:
                authorization = GuardianAuthorization
                # ... your other options

Notes on permissions
--------------------

django-pieguard uses a special `view_modelname` permission to control if user
can view that resource or not. As Django only creates `add`, `change` and
`delete` permissions by default, you need to add the relevant permission on
your model Meta class.

TODO
----

* Tests
* Docs
* Python 3 official support

.. _Django: http://www.djangoproject.com
.. _tastypie: https://github.com/toastdriven/django-tastypie
.. _django-guardian: https://github.com/lukaszb/django-guardian
