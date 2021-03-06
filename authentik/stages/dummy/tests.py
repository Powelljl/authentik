"""dummy tests"""
from django.shortcuts import reverse
from django.test import Client, TestCase
from django.utils.encoding import force_str

from authentik.core.models import User
from authentik.flows.models import Flow, FlowDesignation, FlowStageBinding
from authentik.stages.dummy.forms import DummyStageForm
from authentik.stages.dummy.models import DummyStage


class TestDummyStage(TestCase):
    """Dummy tests"""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username="unittest", email="test@beryju.org")
        self.client = Client()

        self.flow = Flow.objects.create(
            name="test-dummy",
            slug="test-dummy",
            designation=FlowDesignation.AUTHENTICATION,
        )
        self.stage = DummyStage.objects.create(
            name="dummy",
        )
        FlowStageBinding.objects.create(
            target=self.flow,
            stage=self.stage,
            order=0,
        )

    def test_valid_render(self):
        """Test that View renders correctly"""
        response = self.client.get(
            reverse(
                "authentik_flows:flow-executor", kwargs={"flow_slug": self.flow.slug}
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """Test with valid email, check that URL redirects back to itself"""
        url = reverse(
            "authentik_flows:flow-executor", kwargs={"flow_slug": self.flow.slug}
        )
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            force_str(response.content),
            {"type": "redirect", "to": reverse("authentik_core:shell")},
        )

    def test_form(self):
        """Test Form"""
        data = {"name": "test"}
        self.assertEqual(DummyStageForm(data).is_valid(), True)
