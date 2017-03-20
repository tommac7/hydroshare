import os
import tempfile
import shutil

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import Group
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.urlresolvers import reverse

from rest_framework import status

from hs_core import hydroshare
from hs_core.models import BaseResource, ResourceFile
from hs_core.views import create_resource
from hs_core.testing import MockIRODSTestCaseMixin


class TestCreateResourceViewFunctions(MockIRODSTestCaseMixin, TestCase):
    def setUp(self):
        super(TestCreateResourceViewFunctions, self).setUp()
        self.group, _ = Group.objects.get_or_create(name='Hydroshare Author')
        self.username = 'john'
        self.password = 'jhmypassword'
        self.user = hydroshare.create_account(
            'john@gmail.com',
            username=self.username,
            first_name='John',
            last_name='Clarson',
            superuser=False,
            password=self.password,
            groups=[]
        )

        self.factory = RequestFactory()

        self.temp_dir = tempfile.mkdtemp()

        self.raster_tif_file_name = 'raster_tif_valid.tif'
        self.raster_tif_file = 'hs_geo_raster_resource/tests/{}'.format(self.raster_tif_file_name)
        target_temp_raster_tif_file = os.path.join(self.temp_dir, self.raster_tif_file_name)
        shutil.copy(self.raster_tif_file, target_temp_raster_tif_file)
        self.raster_tif_file_obj = open(target_temp_raster_tif_file, 'r')

        self.raster_bad_tif_file_name = 'raster_tif_invalid.tif'
        self.raster_bad_tif_file = 'hs_geo_raster_resource/tests/{}'.format(
            self.raster_bad_tif_file_name)
        target_temp_raster_bad_tif_file = os.path.join(self.temp_dir, self.raster_bad_tif_file_name)
        shutil.copy(self.raster_bad_tif_file, target_temp_raster_bad_tif_file)
        self.raster_bad_tif_file_obj = open(target_temp_raster_bad_tif_file, 'r')

    def tearDown(self):
        super(TestCreateResourceViewFunctions, self).tearDown()
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_create_resource(self):
        # here we are testing the create_resource view function

        # test with no file upload
        post_data = {'resource-type': 'RasterResource',
                     'title': 'Test Raster Resource Creation',
                     'irods_federated': 'true'
                     }
        url = reverse('create_resource')
        request = self.factory.post(url, data=post_data)
        request.user = self.user
        self._set_request_message_attributes(request)
        self._add_session_to_request(request)

        response = create_resource(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        res_id = response.url.split('/')[2]
        self.assertEqual(BaseResource.objects.filter(short_id=res_id).exists(), True)
        hydroshare.delete_resource(res_id)
        self.assertEqual(BaseResource.objects.count(), 0)

        # test with file upload
        self.assertEqual(ResourceFile.objects.count(), 0)
        post_data = {'resource-type': 'RasterResource',
                     'title': 'Test Raster Resource Creation',
                     'irods_federated': 'true',
                     'files': (self.raster_tif_file_name, open(self.raster_tif_file))
                     }
        url = reverse('create_resource')
        request = self.factory.post(url, data=post_data)
        request.user = self.user
        self._set_request_message_attributes(request)
        self._add_session_to_request(request)

        response = create_resource(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        res_id = response.url.split('/')[2]
        self.assertEqual(BaseResource.objects.filter(short_id=res_id).exists(), True)
        # there should be 2 files (tif and vrt) - successful metadata extraction
        self.assertEqual(ResourceFile.objects.count(), 2)

        hydroshare.delete_resource(res_id)

    def test_create_resource_with_invalid_file(self):
        # here we are testing the create_resource view function

        self.assertEqual(BaseResource.objects.count(), 0)
        self.assertEqual(ResourceFile.objects.count(), 0)
        # test with bad tif file - this file should not be uploaded
        post_data = {'resource-type': 'RasterResource',
                     'title': 'Test Raster Resource Creation',
                     'irods_federated': 'true',
                     'files': (self.raster_bad_tif_file_name,
                               open(self.raster_bad_tif_file))
                     }
        url = reverse('create_resource')
        request = self.factory.post(url, data=post_data)
        request.user = self.user
        self._set_request_message_attributes(request)
        self._add_session_to_request(request)

        response = create_resource(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        res_id = response.url.split('/')[2]
        self.assertEqual(BaseResource.objects.filter(short_id=res_id).exists(), True)
        # that bad tif file was not uploaded
        self.assertEqual(ResourceFile.objects.count(), 0)
        hydroshare.delete_resource(res_id)

    def _set_request_message_attributes(self, request):
        # the following 3 lines are for preventing error in unit test due to the view being
        # tested uses messaging middleware
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def _add_session_to_request(self, request):
        """Annotate a request object with a session"""
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
