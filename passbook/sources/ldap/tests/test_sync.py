"""LDAP Source tests"""
from unittest.mock import PropertyMock, patch

from django.test import TestCase

from passbook.core.models import Group, User
from passbook.providers.oauth2.generators import generate_client_secret
from passbook.sources.ldap.models import LDAPPropertyMapping, LDAPSource
from passbook.sources.ldap.sync import LDAPSynchronizer
from passbook.sources.ldap.tasks import sync
from passbook.sources.ldap.tests.utils import _build_mock_connection

LDAP_PASSWORD = generate_client_secret()
LDAP_CONNECTION_PATCH = PropertyMock(return_value=_build_mock_connection(LDAP_PASSWORD))


class LDAPSyncTests(TestCase):
    """LDAP Sync tests"""

    def setUp(self):
        self.source = LDAPSource.objects.create(
            name="ldap",
            slug="ldap",
            base_dn="DC=AD2012,DC=LAB",
            additional_user_dn="ou=users",
            additional_group_dn="ou=groups",
        )
        self.source.property_mappings.set(LDAPPropertyMapping.objects.all())
        self.source.save()

    @patch("passbook.sources.ldap.models.LDAPSource.connection", LDAP_CONNECTION_PATCH)
    def test_sync_users(self):
        """Test user sync"""
        syncer = LDAPSynchronizer(self.source)
        syncer.sync_users()
        self.assertTrue(User.objects.filter(username="user0_sn").exists())
        self.assertFalse(User.objects.filter(username="user1_sn").exists())

    @patch("passbook.sources.ldap.models.LDAPSource.connection", LDAP_CONNECTION_PATCH)
    def test_sync_groups(self):
        """Test group sync"""
        syncer = LDAPSynchronizer(self.source)
        syncer.sync_groups()
        syncer.sync_membership()
        group = Group.objects.filter(name="test-group")
        self.assertTrue(group.exists())

    @patch("passbook.sources.ldap.models.LDAPSource.connection", LDAP_CONNECTION_PATCH)
    def test_tasks(self):
        """Test Scheduled tasks"""
        sync()