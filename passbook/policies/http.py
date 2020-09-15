"""policy http response"""
from typing import Any, Dict, Optional

from django.http.request import HttpRequest
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _

from passbook.core.models import PASSBOOK_USER_DEBUG
from passbook.policies.types import PolicyResult


class AccessDeniedResponse(TemplateResponse):
    """Response used for access denied messages. Can optionally show an error message,
    and if the user is a superuser or has user_debug enabled, shows a policy result."""

    title: str

    error_message: Optional[str] = None
    policy_result: Optional[PolicyResult] = None

    def __init__(self, request: HttpRequest) -> None:
        # For some reason pyright complains about keyword argument usage here
        # pyright: reportGeneralTypeIssues=false
        super().__init__(request=request, template="policies/denied.html")
        self.title = _("Access denied")

    def resolve_context(
        self, context: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        if not context:
            context = {}
        context["title"] = self.title
        if self.error_message:
            context["error"] = self.error_message
        # Only show policy result if user is authenticated and
        # either superuser or has PASSBOOK_USER_DEBUG set
        if self.policy_result:
            if self._request.user and self._request.user.is_authenticated:
                if (
                    self._request.user.is_superuser
                    or self._request.user.attributes.get(PASSBOOK_USER_DEBUG, False)
                ):
                    context["policy_result"] = self.policy_result
        return context