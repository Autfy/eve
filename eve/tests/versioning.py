# -*- coding: utf-8 -*-
from bson import ObjectId

import eve
import json
from eve import Eve
from eve.tests import TestBase
from eve import ETAG


class TestVersioningBase(TestBase):
    def setUp(self):
        super(TestVersioningBase, self).setUp()

        self.version_field = self.app.config['VERSION']
        self.latest_version_field = self.app.config['LATEST_VERSION']

    def assertVersion(self, response, version):
        self.assertTrue(self.version_field in response)
        self.assertEquals(response[self.version_field], version)

    def assertLatestVersion(self, response, latest_version):
        self.assertTrue(self.latest_version_field in response)
        self.assertEquals(response[self.latest_version_field], latest_version)


class TestNormalVersioning(TestVersioningBase):
    def setUp(self):
        super(TestNormalVersioning, self).setUp()
        # self.app = Eve(settings=self.settings_file, auth=ValidBasicAuth)
        # self.test_client = self.app.test_client()
        # self.content_type = ('Content-Type', 'application/json')
        # self.valid_auth = [('Authorization', 'Basic YWRtaW46c2VjcmV0'),
        #                    self.content_type]
        # self.invalid_auth = [('Authorization', 'Basic IDontThinkSo'),
        #                      self.content_type]
        # for _, schema in self.app.config['DOMAIN'].items():
        #     schema['allowed_roles'] = ['admin']
        #     schema['allowed_item_roles'] = ['admin']
        # self.app.set_defaults()

    def assertShadowDocument(self):
        self.assertTrue(True)

    def test_insert_shadow_document_simple(self):
        """Make sure that Eve actually saves a copy of the document in the
        parallel versions collection when the entire document is version
        controlled.
        """
        # test single post
        #todo: be sure to test _version==2 here

        # test put

        # test patch

        # Todo: do I also need to test POST/array?
        self.assertTrue(True)

    def test_insert_shadow_document_complex(self):
        """Make sure that Eve actually saves a copy of the document in the
        parallel versions collection when the entire document is version
        controlled.
        """
        # test single post
        #todo: be sure to test _version==2 here

        # test put

        # test patch

        # Todo: do I also need to test POST/array?
        self.assertTrue(True)

    def test_get_and_getitem_latest_version_simple(self):
        """ Make sure that Eve is correctly synthesizing the latest version of a
        document when the entire document is version controlled.
        """
        # put a change

        # get the latest version and make sure it matches
        self.assertTrue(True)

    def test_get_and_getitem_latest_version_complex(self):
        """ Make sure that Eve is correctly synthesizing the latest version of a
        document when only some fields of a document are version controlled.
        """
        # put a change

        # get the latest version and make sure it matches
        self.assertTrue(True)

    def test_get_old_verion_simple(self):
        """ Make sure that Eve is correctly synthesizing the old version of a
        document when the entire document is version controlled.
        """
        # test get and getitem
        # put a change

        # get the previous version and make sure it matches
        self.assertTrue(True)

    def test_get_old_verion_complex(self):
        """ Make sure that Eve is correctly synthesizing the old version of a
        document when only some fields of a document are version controlled.
        """
        # test get and getitem
        # put a change

        # get the previous version and make sure it matches
        self.assertTrue(True)

    def test_getitem_verion_unknown(self):
        """ Make sure that Eve return a nice error when requesting an unknown
        version.
        """

        self.assertTrue(True)

    def test_getitem_verion_badformat(self):
        """ Make sure that Eve return a nice error when requesting an unknown
        version.
        """
        self.assertTrue(True)

    def test_getitem_verion_all(self):
        # test with HATEOS on and off
        self.assertTrue(True)

    def test_getitem_verion_list(self):
        # test with HATEOS on and off
        # note - i might not even add this feature, is essentially ?version=all with a projection
        self.assertTrue(True)

    def test_getitem_verion_diffs(self):
        # test with HATEOS on and off
        self.assertTrue(True)

    def test_data_relation_with_version(self):
        """ Make sure that Eve correctly validates a data_relation with a
        version and returns the version with the data_relation in the response.
        """
        # test good id and good version

        # test good id and bad version

        # test bad id
        self.assertTrue(True)

    def test_data_relation_without_version(self):
        """ Make sure that Eve still correctly handles vanilla data_relations
        when versioning is turned on.
        """
        self.assertTrue(True)


class TestLateVersioning(TestVersioningBase):
    def setUp(self):
        super(TestLateVersioning, self).setUp()

        # turn on version after data has been inserted into the db
        for resource, settings in self.app.config['DOMAIN'].items():
            settings['versioning'] = True
            settings['datasource'].pop('projection', None)
            self.app.register_resource(resource, settings)

    def test_get(self):
        """ Make sure that Eve returns version = 0 for documents that haven't
        been modified since version control has been turned on.
        """
        response, status = self.get(self.known_resource)
        self.assert200(status)
        items = response['_items']
        self.assertEqual(len(items), self.app.config['PAGINATION_DEFAULT'])
        for item in items:
            self.assertVersion(item, 0)
            self.assertLatestVersion(item, 0)

    def test_getitem(self):
        """ Make sure that Eve returns version = 0 for documents that haven't
        been modified since version control has been turned on.
        """
        response, status = self.get(self.known_resource, item=self.item_id)
        self.assert200(status)
        self.assertVersion(response, 0)
        self.assertLatestVersion(response, 0)

    def test_put(self):
        """ Make sure that Eve still sets version = 1 for documents that where
        already in the database before version control was turned on.
        """
        changes = {"ref": "this is a different value"}
        response, status = self.put(self.item_id_url, data=changes,
                             headers=[('If-Match', self.item_etag)])
        self.assert200(status)
        self.assertVersion(response, 1)
        self.assertLatestVersion(response, 1)

        # make sure that this saved to the db too (if it didn't, version == 0)
        response2, status = self.get(self.known_resource, item=self.item_id)
        self.assert200(status)
        self.assertVersion(response2, 1)
        self.assertLatestVersion(response2, 1)
        self.assertEqual(response[ETAG], response2[ETAG])

    def test_patch(self):
        """ Make sure that Eve still sets version = 1 for documents that where
        already in the database before version control was turned on.
        """
        changes = {"ref": "this is a different value"}
        response, status = self.patch(self.item_id_url, data=changes,
                             headers=[('If-Match', self.item_etag)])
        self.assert200(status)
        self.assertVersion(response, 1)
        self.assertLatestVersion(response, 1)

        # make sure that this saved to the db too (if it didn't, version == 0)
        response2, status = self.get(self.known_resource, item=self.item_id)
        self.assert200(status)
        self.assertVersion(response2, 1)
        self.assertLatestVersion(response2, 1)
        self.assertEqual(response[ETAG], response2[ETAG])

    def test_data_relation_with_version(self):
        """
        """
        #todo: any special considerations for a data relation version to a recently version collection?!
        