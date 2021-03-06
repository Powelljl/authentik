"""OTP Time urls"""
from django.urls import path

from authentik.stages.authenticator_totp.views import DisableView, UserSettingsView

urlpatterns = [
    path(
        "<uuid:stage_uuid>/settings/", UserSettingsView.as_view(), name="user-settings"
    ),
    path("<uuid:stage_uuid>/disable/", DisableView.as_view(), name="disable"),
]
