from rest_framework import viewsets

from core.models import CheckIn, IssueDetail, Person
from core.serializers import (CheckInSerializer,
                              IssueDetailSerializer,
                              PersonSerializer)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class CheckInViewSet(viewsets.ModelViewSet):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer


class IssueDetailViewSet(viewsets.ModelViewSet):
    queryset = IssueDetail.objects.all()
    serializer_class = IssueDetailSerializer
