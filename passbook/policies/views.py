"""passbook access helper classes"""
from typing import Any, Optional

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext as _
from django.views.generic.base import View
from structlog import get_logger

from passbook.core.models import Application, Provider, User
from passbook.flows.views import SESSION_KEY_APPLICATION_PRE
from passbook.policies.engine import PolicyEngine
from passbook.policies.http import AccessDeniedResponse
from passbook.policies.types import PolicyResult

LOGGER = get_logger()


class BaseMixin:
    """Base Mixin class, used to annotate View Member variables"""

    request: HttpRequest


class PolicyAccessView(AccessMixin, View):
    """Mixin class for usage in Authorization views.
    Provider functions to check application access, etc"""

    provider: Provider
    application: Application

    def resolve_provider_application(self):
        """Resolve self.provider and self.application. *.DoesNotExist Exceptions cause a normal
        AccessDenied view to be shown. An Http404 exception
        is not caught, and will return directly"""
        raise NotImplementedError

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            self.resolve_provider_application()
        except (Application.DoesNotExist, Provider.DoesNotExist):
            return self.handle_no_permission_authenticated()
        # Check if user is unauthenticated, so we pass the application
        # for the identification stage
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        # Check permissions
        result = self.user_has_access()
        if not result.passing:
            return self.handle_no_permission_authenticated(result)
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self) -> HttpResponse:
        """User has no access and is not authenticated, so we remember the application
        they try to access and redirect to the login URL. The application is saved to show
        a hint on the Identification Stage what the user should login for."""
        if self.application:
            self.request.session[SESSION_KEY_APPLICATION_PRE] = self.application
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name(),
        )

    def handle_no_permission_authenticated(
        self, result: Optional[PolicyResult] = None
    ) -> HttpResponse:
        """Function called when user has no permissions but is authenticated"""
        response = AccessDeniedResponse(self.request)
        if result:
            response.policy_result = result
        return response

    def user_has_access(self, user: Optional[User] = None) -> PolicyResult:
        """Check if user has access to application."""
        user = user or self.request.user
        policy_engine = PolicyEngine(
            self.application, user or self.request.user, self.request
        )
        policy_engine.build()
        result = policy_engine.result
        LOGGER.debug(
            "AccessMixin user_has_access",
            user=user,
            app=self.application,
            result=result,
        )
        if not result.passing:
            for message in result.messages:
                messages.error(self.request, _(message))
        return result