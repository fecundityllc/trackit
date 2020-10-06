import os
import re

from github import Github
from rest_framework import status
from rest_framework.response import Response
from slack import WebClient


def get_issue_title(url):
    github_handle = Github(os.environ.get('GITHUB'))
    url = url.split("/")
    repo_name = "/".join(url[3:5])
    repository = github_handle.get_repo(repo_name)
    issue = repository.get_issue(number=int(url[-1]))
    return issue.title


def get_email_from_slack_response(request):
    client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    response = client.users_info(user=request.POST['user_id'])
    return response['user']['profile']['email']


def get_checkin_details(request):
    params = extract_params(request)
    response = params_validation(params)
    checkin_details = dict()
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        return response, checkin_details
    if os.getenv("SLACK_BOT_TOKEN") is None:
        return Response(
            "Error: Please provide slack bot token",
            status=status.HTTP_404_NOT_FOUND), checkin_details
    checkin_details['issue'] = params[0]
    checkin_details['time_spent'] = params[1]
    checkin_details['description'] = params[2]
    return response, checkin_details


def extract_params(request):
    params = request.POST['text']
    params = " ".join(re.split(r"\s+", params, flags=re.UNICODE))
    params = params.split(" ", 2)
    return params


def params_validation(params):
    if len(params) < 3:
        return Response(
            "Error: Please provide all paramters. url hours_spent description\
            e.g /checkin https://github.com/unationmain/api-backend/issues/3\
            8 Fixed styles", status=status.HTTP_400_BAD_REQUEST)
    if len(params[0]) > 500:
        return Response(
            "Error: Size of URL must be less than 200 characters",
            status=status.HTTP_400_BAD_REQUEST)
    if len(params[2]) > 200:
        return Response(
            "Error: Please provide short description \
            (less than 200 characters)", status=status.HTTP_400_BAD_REQUEST)
    return Response("Parameters are fine", status=status.HTTP_200_OK)
