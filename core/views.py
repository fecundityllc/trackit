from rest_framework import viewsets
from core.models import Person, CheckIn, IssueDetail
from core.serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = EmployeeSerializer
