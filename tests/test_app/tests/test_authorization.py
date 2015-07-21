from django.test import TestCase
from tastypie.test import ResourceTestCase
from test_app.api import ProjectResource
from guardian.shortcuts import assign_perm

from pieguard.authorization import GuardianAuthorization

from test_app.tests import factories
from test_app.models import Project


class GuardianAuthorizationResourceTest(ResourceTestCase):

    def setUp(self):
        super(GuardianAuthorizationResourceTest, self).setUp()

        self.username = 'jondue'
        self.password = '123456'

        self.user = factories.UserFactory(
            username=self.username,
            password=self.password
            )

        self.projects = []
        for i in xrange(0, 10):
            self.projects.append(factories.ProjectFactory())

        self.api_url = '/api/v1/project/'

    def get_credentials(self):
        return self.create_basic(self.username, self.password)

    def build_detail_url(self, project):
        return '{}{}/'.format(self.api_url, project.id)

    def build_data_to_post(self):
        return {
            'name': 'new project'
        }

    def build_data_to_change_detail(self, project):
        return {
            'id': project.id, 'name': project.name + ' changed'
        }

    def build_data_to_put(self, number_of_projects=10):
        put_data = {'list': []}
        for project in self.projects[0:number_of_projects]:
            put_data['list'].append(
                self.build_data_to_change_detail(project)
                )

        return put_data

    def build_data_to_patch(self, number_of_projects=10):
        return self.build_data_to_put(number_of_projects)

    def test_get_list_without_permission(self):
        resp = self.api_client.get(
            self.api_url,
            format='json',
            authentication=self.get_credentials()
        )

        self.assertValidJSONResponse(resp)
        self.assertEqual(
            len(self.deserialize(resp)['objects']),
            0
            )

    def test_get_list_with_global_permission(self):
        assign_perm('test_app.view_project', self.user)

        resp = self.api_client.get(
            self.api_url,
            format='json',
            authentication=self.get_credentials()
        )

        self.assertValidJSONResponse(resp)
        self.assertEqual(
            len(self.deserialize(resp)['objects']),
            len(self.projects)
            )

    def test_get_list_with_permission_to_all_objects(self):
        for project in self.projects:
            assign_perm('view_project', self.user, project)

        resp = self.api_client.get(
            self.api_url,
            format='json',
            authentication=self.get_credentials()
        )

        self.assertValidJSONResponse(resp)
        self.assertEqual(
            len(self.deserialize(resp)['objects']),
            len(self.projects)
            )

    def test_get_list_with_limited_permission_to_objects(self):
        for project in self.projects[0:5]:
            assign_perm('view_project', self.user, project)

        resp = self.api_client.get(
            self.api_url,
            format='json',
            authentication=self.get_credentials()
        )

        self.assertValidJSONResponse(resp)
        self.assertEqual(
            len(self.deserialize(resp)['objects']),
            5
            )

    def test_post_list_without_access(self):

        resp = self.api_client.post(
            self.api_url,
            format='json',
            authentication=self.get_credentials(),
            data=self.build_data_to_post()
            )

        self.assertHttpUnauthorized(resp)

    def test_post_list_with_permission(self):
        assign_perm('test_app.add_project', self.user)

        # [fixme] - should check firstly global permissions!

        resp = self.api_client.post(
            self.api_url,
            format='json',
            authentication=self.get_credentials(),
            data=self.build_data_to_post()
            )

        self.assertHttpCreated(resp)

    def test_put_list_with_global_permission(self):
        assign_perm('test_app.change_project', self.user)

        resp = self.api_client.put(
            self.api_url,
            format='json',
            authentication=self.get_credentials(),
            data=self.build_data_to_put(),
            )

        self.assertTrue(resp.status_code, 202)

    def test_put_list_with_limited_permission(self):
        for project in self.projects[0:5]:
            assign_perm('change_project', self.user, project)

        resp = self.api_client.put(
            self.api_url,
            format='json',
            authentication=self.get_credentials(),
            data=self.build_data_to_put(),
            )

        self.assertHttpBadRequest(resp)

    def test_put_list_with_permissions_by_object(self):
        for project in self.projects:
            assign_perm('change_project', self.user, project)

        resp = self.api_client.put(
            self.api_url,
            format='json',
            authentication=self.get_credentials(),
            data=self.build_data_to_put(),
            )

        self.assertTrue(resp.status_code, 202)

    def test_patch_list_with_global_permission(self):
        assign_perm('test_app.change_project', self.user)

        resp = self.api_client.patch(
            self.api_url,
            format='json',
            authentication=self.get_credentials(),
            data=self.build_data_to_patch(),
            )

        self.assertTrue(resp.status_code, 202)

    def test_patch_list_with_limited_permission(self):
        for project in self.projects[0:5]:
            assign_perm('change_project', self.user, project)

        resp = self.api_client.patch(
            self.api_url,
            format='json',
            authentication=self.get_credentials(),
            data=self.build_data_to_patch(),
            )

        self.assertHttpBadRequest(resp)

    def test_patch_list_with_permissions_by_object(self):
        for project in self.projects:
            assign_perm('change_project', self.user, project)

        resp = self.api_client.patch(
            self.api_url,
            format='json',
            authentication=self.get_credentials(),
            data=self.build_data_to_patch(),
            )

        self.assertTrue(resp.status_code, 202)

    def test_get_detail_without_permission(self):
        project = self.projects[0]

        resp = self.api_client.get(
            self.build_detail_url(project),
            format='json',
            authentication=self.get_credentials()
        )

        self.assertHttpUnauthorized(resp)

    def test_get_detail_with_global_permission(self):
        assign_perm('test_app.view_project', self.user)
        project = self.projects[0]

        resp = self.api_client.get(
            self.build_detail_url(project),
            format='json',
            authentication=self.get_credentials()
        )

        self.assertValidJSONResponse(resp)

    def test_get_detail_with_permission(self):
        project = self.projects[0]
        assign_perm('view_project', self.user, project)

        resp = self.api_client.get(
            self.build_detail_url(project),
            format='json',
            authentication=self.get_credentials()
        )

        self.assertValidJSONResponse(resp)

    def test_put_detail_with_permission(self):
        project = self.projects[0]
        assign_perm('change_project', self.user, project)

        resp = self.api_client.put(
            self.build_detail_url(project),
            format='json',
            authentication=self.get_credentials(),
            data=self.build_data_to_change_detail(project),
        )

        self.assertTrue(resp.status_code, 202)

    def test_put_detail_without_permission(self):
        project = self.projects[0]

        resp = self.api_client.put(
            self.build_detail_url(project),
            format='json',
            authentication=self.get_credentials(),
            data=self.build_data_to_change_detail(project),
        )

        self.assertHttpUnauthorized(resp)

    def test_patch_detail_with_permission(self):
        project = self.projects[0]
        assign_perm('change_project', self.user, project)

        resp = self.api_client.patch(
            self.build_detail_url(project),
            format='json',
            authentication=self.get_credentials(),
            data=self.build_data_to_change_detail(project),
        )

        self.assertTrue(resp.status_code, 202)

    def test_patch_detail_without_permission(self):
        project = self.projects[0]

        resp = self.api_client.patch(
            self.build_detail_url(project),
            format='json',
            authentication=self.get_credentials(),
            data=self.build_data_to_change_detail(project),
        )

        self.assertHttpUnauthorized(resp)

    def test_delete_detail_with_permission(self):
        project = self.projects[0]
        assign_perm('delete_project', self.user, project)

        resp = self.api_client.delete(
            self.build_detail_url(project),
            format='json',
            authentication=self.get_credentials(),
        )

        self.assertTrue(resp.status_code, 202)

    def test_delete_detail_without_permission(self):
        project = self.projects[0]

        resp = self.api_client.delete(
            self.build_detail_url(project),
            format='json',
            authentication=self.get_credentials(),
        )

        self.assertHttpUnauthorized(resp)



