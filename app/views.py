from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import ValidationError
from app.serializers import ApplicationDetailsSerializer, GetApplicationsQuerySerializer
from app.services.qa import QAService


class AppViewSet(ViewSet):
    qa_service = QAService()

    def list(self, request):
        query_ser = GetApplicationsQuerySerializer(data=request.query_params)
        if not query_ser.is_valid():
            raise ValidationError(query_ser.errors)
        applications = self.app_service.get_applications(**query_ser.data)
        return Response(ApplicationDetailsSerializer(applications, many=True).data)
