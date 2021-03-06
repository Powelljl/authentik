"""evaluator tests"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from guardian.shortcuts import get_anonymous_user

from authentik.policies.exceptions import PolicyException
from authentik.policies.expression.evaluator import PolicyEvaluator
from authentik.policies.expression.models import ExpressionPolicy
from authentik.policies.types import PolicyRequest


class TestEvaluator(TestCase):
    """Evaluator tests"""

    def setUp(self):
        self.request = PolicyRequest(user=get_anonymous_user())

    def test_full(self):
        """Test full with Policy instance"""
        policy = ExpressionPolicy(name="test", expression="return 'test'")
        policy.save()
        request = PolicyRequest(get_anonymous_user())
        result = policy.passes(request)
        self.assertTrue(result.passing)

    def test_valid(self):
        """test simple value expression"""
        template = "return True"
        evaluator = PolicyEvaluator("test")
        evaluator.set_policy_request(self.request)
        self.assertEqual(evaluator.evaluate(template).passing, True)

    def test_messages(self):
        """test expression with message return"""
        template = 'ak_message("some message");return False'
        evaluator = PolicyEvaluator("test")
        evaluator.set_policy_request(self.request)
        result = evaluator.evaluate(template)
        self.assertEqual(result.passing, False)
        self.assertEqual(result.messages, ("some message",))

    def test_invalid_syntax(self):
        """test invalid syntax"""
        template = ";"
        evaluator = PolicyEvaluator("test")
        evaluator.set_policy_request(self.request)
        with self.assertRaises(PolicyException):
            evaluator.evaluate(template)

    def test_validate(self):
        """test validate"""
        template = "True"
        evaluator = PolicyEvaluator("test")
        result = evaluator.validate(template)
        self.assertEqual(result, True)

    def test_validate_invalid(self):
        """test validate"""
        template = ";"
        evaluator = PolicyEvaluator("test")
        with self.assertRaises(ValidationError):
            evaluator.validate(template)
