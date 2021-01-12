"""event_matcher tests"""
from django.test import TestCase
from guardian.shortcuts import get_anonymous_user

from authentik.events.models import Event, EventAction
from authentik.policies.event_matcher.models import EventMatcherPolicy
from authentik.policies.types import PolicyRequest


class TestEventMatcherPolicy(TestCase):
    """EventMatcherPolicy tests"""

    def test_drop_action(self):
        """Test drop event"""
        event = Event.new(EventAction.LOGIN)
        request = PolicyRequest(get_anonymous_user())
        request.context["event"] = event
        policy: EventMatcherPolicy = EventMatcherPolicy.objects.create(
            action=EventAction.LOGIN_FAILED
        )
        response = policy.passes(request)
        self.assertFalse(response.passing)
        self.assertTupleEqual(response.messages, ("Action did not match.",))

    def test_drop_client_ip(self):
        """Test drop event"""
        event = Event.new(EventAction.LOGIN)
        event.client_ip = "1.2.3.4"
        request = PolicyRequest(get_anonymous_user())
        request.context["event"] = event
        policy: EventMatcherPolicy = EventMatcherPolicy.objects.create(
            client_ip="1.2.3.5"
        )
        response = policy.passes(request)
        self.assertFalse(response.passing)
        self.assertTupleEqual(response.messages, ("Client IP did not match.",))

    def test_drop_app(self):
        """Test drop event"""
        event = Event.new(EventAction.LOGIN)
        event.app = "foo"
        request = PolicyRequest(get_anonymous_user())
        request.context["event"] = event
        policy: EventMatcherPolicy = EventMatcherPolicy.objects.create(app="bar")
        response = policy.passes(request)
        self.assertFalse(response.passing)
        self.assertTupleEqual(response.messages, ("App did not match.",))

    def test_passing(self):
        """Test passing event"""
        event = Event.new(EventAction.LOGIN)
        event.client_ip = "1.2.3.4"
        request = PolicyRequest(get_anonymous_user())
        request.context["event"] = event
        policy: EventMatcherPolicy = EventMatcherPolicy.objects.create(
            client_ip="1.2.3.4"
        )
        response = policy.passes(request)
        self.assertTrue(response.passing)

    def test_invalid(self):
        """Test passing event"""
        request = PolicyRequest(get_anonymous_user())
        policy: EventMatcherPolicy = EventMatcherPolicy.objects.create(
            client_ip="1.2.3.4"
        )
        response = policy.passes(request)
        self.assertFalse(response.passing)