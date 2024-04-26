from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from refsystem.models import UsedCode
from refsystem.serializers import UsedCodeSerializer


class UsedCodeViewSet(viewsets.ModelViewSet):

    queryset = UsedCode.objects.all()
    serializer_class = UsedCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def set_code(self, request, pk=None):
        serializer = UsedCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        response_data = serializer.set_code()
        return Response(response_data)
