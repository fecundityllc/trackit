from dateutil import parser
from django.db.models import ProtectedError
from django.test import TestCase
from django.utils import timezone

from core.models import CheckIn, IssueDetail, Person
from core.utils import get_issue_title


class TrackitTestCases(TestCase):
    payload = {
        "person": {
            "name": "mohsan",
            "email": "mohsan@fecundity.io"
        },
        "issue": {
            "issue_url": "https://github.com/fecundityllc/trackit/issues/12"
        },
        "checkin": {
            "name": "someone",
            "person": "someone@fecundity.io",
            "issue": "https://github.com/fecundityllc/trackit/issues/12",
            "time_spent": 3.4,
            "description": "testing"
        }
    }

    def create_person(self):
        person, _ = Person.objects.get_or_create(
            name="Alex", email="alex@somewhere.com")
        return person

    def create_issue(self):
        url = "https://github.com/fecundityllc/trackit/issues/12"
        issue = {
            "issue_url": url,
            "title": get_issue_title(url)
        }
        issue, _ = IssueDetail.objects.get_or_create(**issue)
        return issue

    def create_checkin(self):
        data = {
            "person": self.create_person(),
            "issue": self.create_issue(),
            "time_spent": 2.4,
            "description": 'I did this'
        }
        checkin, _ = CheckIn.objects.get_or_create(**data)
        return checkin

    def test_checkin_count(self):
        self.create_checkin()
        self.assertEqual(len(CheckIn.objects.all()), 1)

    def test_checkin_data(self):
        person = self.create_person()
        issue = self.create_issue()
        checkin = self.create_checkin()
        self.assertEqual(checkin.person, person)
        self.assertEqual(checkin.issue, issue)
        self.assertEqual(timezone.localdate(
            checkin.created_at), timezone.now().date())

    def test_person_deletion_checkin(self):
        person = self.create_person()
        self.create_checkin()
        self.assertRaises(ProtectedError, person.delete)

    def test_issue_deletion_checkin(self):
        issue = self.create_issue()
        self.create_checkin()
        self.assertRaises(ProtectedError, issue.delete)

    def test_person_repr(self):
        person = self.create_person()
        self.assertEqual(str(person), person.email)

    def test_issue_repr(self):
        issue = self.create_issue()
        self.assertEqual(str(issue), "trackit #12")

    def test_checkin_api(self):
        response = self.client.post(
            "/checkin/", data=self.payload.get('checkin'))
        self.assertEqual(response.status_code, 201)
        checkin_data = self.payload.get('checkin')
        checkin = CheckIn.objects.get(id=response.data['id'])
        self.assertEqual(str(checkin.person), checkin_data['person'])
        self.assertEqual(checkin.issue.issue_url, checkin_data['issue'])
        self.assertEqual(timezone.localdate(
            checkin.created_at), timezone.now().date())
        self.assertEqual(checkin.time_spent, checkin_data['time_spent'])

        response = self.client.post(
            "/checkin/", data=self.payload.get('checkin'))
        self.assertEqual(response.status_code, 201)
        previous_time = checkin.time_spent
        checkin.refresh_from_db()

        self.assertEqual(checkin.time_spent, previous_time +
                         checkin_data['time_spent'])

    def test_checkin_get(self):
        response = self.client.post(
            "/checkin/", data=self.payload.get('checkin'))
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/checkin/')
        self.assertEqual(response.status_code, 200)
        data = response.data['results'][0]
        person = Person.objects.get(email=data['person'])
        self.assertEqual(data['person'], str(person))
        self.assertEqual(data['time_spent'],
                         self.payload["checkin"]["time_spent"])
        date = parser.parse(data['created_at'])
        self.assertEqual(date.date(), timezone.now().date())

    def test_person_post(self):
        response = self.client.post('/person/', data=self.payload["person"])
        self.assertEqual(response.status_code, 201)

        person = Person.objects.get(id=response.data['id'])
        self.assertEqual(person.name, self.payload['person']['name'])
        self.assertEqual(person.email, self.payload['person']['email'])
