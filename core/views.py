import json
import os
from threading import Thread

import requests
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view

from core import serializers
from core.models import CheckIn, IssueDetail, Person
from core.utils import get_checkin_details


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
    except Exception:
        HttpResponse(
            "Error: unable to process your request ",
            status.HTTP_200_OK
        )
    return HttpResponse(
        "Got your command. Let me process",
        status.HTTP_200_OK
    )


def process_request(response_url, request):
    response, checkin_details = get_checkin_details(request)
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        requests.post(response_url, data=json.dumps({"text": response.data}))
    else:
        try:
            payload = dict(checkin_details)
            response = requests.post(
                str(os.environ.get('DOMAIN')) + '/checkin/',
                data=payload
            )
            data = dict()
            data["text"] = "Name: " + payload["name"] \
                + "\nIssue: " + payload["issue"] \
                + "\nHours spent: " + payload["time_spent"] \
                + "\nDescription: " + payload["description"]
            data["response_type"] = "in_channel"
            requests.post(response_url, data=json.dumps(data))
        except Exception:
            requests.post(
                response_url,
                data="{'text': 'Unable to proccess your command'}")
