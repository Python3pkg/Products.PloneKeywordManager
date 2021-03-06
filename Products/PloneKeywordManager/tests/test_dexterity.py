# -*- coding: utf-8 -*-

from plone.dexterity.fti import DexterityFTI
from Products.PloneKeywordManager.tests.base import PKMTestCase


class DexterityContentTestCase(PKMTestCase):
    """Test the keyword manager with Dexterity content types"""

    def setUp(self):
        super(DexterityContentTestCase, self).setUp()
        self.portal.portal_types._setObject(
            'test_type', DexterityFTI('test_type'))
        test_type = self.portal.portal_types.test_type
        test_type.klass = 'plone.dexterity.content.Item'
        test_type.behaviors = (
            'plone.app.dexterity.behaviors.metadata.IDublinCore',
        )
        self.portal.invokeFactory('test_type', 'test_content')
        self.content = self.portal['test_content']
        self.content.setSubject('Keyword1 Keyword2 Keyword3'.split())
        self.content.reindexObject()

    def test_dexterity_keywords_changeto(self):
        self._action_change(['Keyword1', 'Keyword2', ], 'Keyword4')
        self.assertEqual(sorted(self.content.Subject()),
                         ['Keyword3', 'Keyword4', ],)

    def test_dexterity_keywords_delete(self):
        self._action_delete(['Keyword3', ])
        self.assertEqual(sorted(self.content.Subject()),
                         ['Keyword1', 'Keyword2', ],)
