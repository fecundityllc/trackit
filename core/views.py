from rest_framework import viewsets

from core import serializers
from core.models import CheckIn, IssueDetail, Person


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = serializers.PersonSerializer


class CheckInViewSet(viewsets.ModelViewSet):
    queryset = CheckIn.objects.all()
    serializer_class = serializers.CheckInSerializer


class IssueDetailViewSet(viewsets.ModelViewSet):
    queryset = IssueDetail.objects.all()
    serializer_class = serializers.IssueDetailSerializer
