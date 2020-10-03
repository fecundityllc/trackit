from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class IssueDetail(models.Model):
    title = models.CharField(max_length=255)
    issue_url = models.URLField(max_length=500)
    
    def __str__(self):
        issue = self.issue_url.split('/')
        try:
            return f'{issue[-3]} #{issue[-1]}'
        except IndexError:
            return self.issue_url


class CheckIn(models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    issue = models.ForeignKey(IssueDetail, on_delete=models.PROTECT)
    time_spent = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=100)
