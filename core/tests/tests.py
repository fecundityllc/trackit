from dateutil import parser
from django.db.models import ProtectedError
from django.test import TestCase
from django.utils import timezone

from core.models import CheckIn, IssueDetail, Person
from core.utils import get_issue_title


class TrackitTestCases(TestCase):
    def setUp(self):
        self.person = Person.objects.create(
            name="someone", email="someone@example.io")

        url = "https://github.com/fecundityllc/trackit/issues/12"
        self.issue = IssueDetail.objects.create(
            title=get_issue_title(url), issue_url=url)
        self.checkin = CheckIn.objects.create(
            issue=self.issue,
            person=self.person,
            time_spent=2.4,
            description="I did this.")
    payload = {
        "person": {
            "name": "someone",
            "email": "someone@fecundity.io"
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

    def test_checkin_count(self):
        self.assertEqual(len(CheckIn.objects.all()), 1)

    def test_checkin_data(self):
        self.assertEqual(self.checkin.person, self.person)
        self.assertEqual(self.checkin.issue, self.issue)
        self.assertEqual(timezone.localdate(
            self.checkin.created_at), timezone.now().date())

    def test_person_deletion_checkin(self):
        self.assertRaises(ProtectedError, self.person.delete)

    def test_issue_deletion_checkin(self):
        self.assertRaises(ProtectedError, self.issue.delete)

    def test_person_repr(self):
        self.assertEqual(str(self.person), self.person.email)

    def test_issue_repr(self):
        self.assertEqual(str(self.issue), "trackit #12")

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
        response = self.client.get('/checkin/')
        self.assertEqual(response.status_code, 200)
        data = response.data['results'][0]
        self.assertEqual(data['person'], str(self.person))
        self.assertEqual(data['time_spent'],
                         self.checkin.time_spent)
        date = parser.parse(data['created_at'])
        self.assertEqual(date.date(), timezone.now().date())

    def test_person_post(self):
        response = self.client.post('/person/', data=self.payload["person"])
        self.assertEqual(response.status_code, 201)

        person = Person.objects.get(id=response.data['id'])
        self.assertEqual(person.name, self.payload['person']['name'])
        self.assertEqual(person.email, self.payload['person']['email'])
