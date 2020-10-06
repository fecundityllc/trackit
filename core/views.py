import json
import os
from threading import Thread

import requests
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view

from core import serializers
from core.models import CheckIn, IssueDetail, Person
from core.utils import get_checkin_details, get_email_from_slack_response


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = serializers.PersonSerializer


class CheckInViewSet(viewsets.ModelViewSet):
    queryset = CheckIn.objects.all()
    serializer_class = serializers.CheckInSerializer


class IssueDetailViewSet(viewsets.ModelViewSet):
    queryset = IssueDetail.objects.all()
    serializer_class = serializers.IssueDetailSerializer


@api_view(['POST'])
def StoreCheckinDetails(request):
    response_url = request.POST['response_url']
    try:
        thread = Thread(target=process_request, args=(response_url, request))
        thread.start()
    except Exception as e:
        print("Error: unable to process your request " + str(e))
    return HttpResponse("Got your command. Let me process", status.HTTP_200_OK)


def process_request(response_url, request):
    response, checkin_details = get_checkin_details(request)
    payload = dict()
    payload['name'] = request.POST['user_name']
    payload['person'] = get_email_from_slack_response(request)
    payload.update(checkin_details)
    requests.post(str(os.environ.get('DOMAIN')) + '/checkin/', data=payload)
    data = dict()
    data["text"] = "Thank You for checkin"
    data["response_type"] = "ephemeral"
    requests.post(response_url, data=json.dumps(data))
