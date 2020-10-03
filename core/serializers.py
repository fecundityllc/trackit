
from django.utils import timezone
from rest_framework import serializers

from core import utils
from core.models import CheckIn, IssueDetail, Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


class CheckInSerializer(serializers.HyperlinkedModelSerializer):
    person = serializers.EmailField()
    issue = serializers.URLField()

    class Meta:
        model = CheckIn
        fields = ["id",
                  "person",
                  "issue",
                  "created_at",
                  "updated_at",
                  "time_spent",
                  "description"]

    def create(self, validated_data):
        email = validated_data.pop('person')
        default = {"name": "Unkwon"}
        person, _ = Person.objects.get_or_create(email=email,
                                                 defaults=default)
        issue = validated_data.pop('issue')
        issue_title = utils.get_issue_title(issue)
        issue, _ = IssueDetail.objects.get_or_create(issue_url=issue,
                                                     title=issue_title)
        try:
            checkin = CheckIn.objects.get(
                person=person,
                issue=issue,
                created_at__date=timezone.now().date())

            checkin.time_spent += validated_data.get('time_spent')
            checkin.save()
            return checkin
        except CheckIn.DoesNotExist:
            checkin = CheckIn.objects.create(**validated_data,
                                             person=person,
                                             issue=issue)
            return checkin


class IssueDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueDetail
        fields = "__all__"
