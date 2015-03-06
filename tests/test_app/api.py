from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from pieguard.authorization import GuardianAuthorization
from test_app.models import Project


class ProjectResource(ModelResource):
    class Meta:
        resource_name = 'project'
        default_format = 'application/json'
        queryset = Project.objects.all()
        authentication = BasicAuthentication()
        authorization = GuardianAuthorization()
        abstract = True
