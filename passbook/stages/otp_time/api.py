"""OTPTimeStage API Views"""
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from passbook.stages.otp_time.models import OTPTimeStage


class OTPTimeStageSerializer(ModelSerializer):
    """OTPTimeStage Serializer"""

    class Meta:

        model = OTPTimeStage
        fields = ["pk", "name", "digits"]


class OTPTimeStageViewSet(ModelViewSet):
    """OTPTimeStage Viewset"""

    queryset = OTPTimeStage.objects.all()
    serializer_class = OTPTimeStageSerializer