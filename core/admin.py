from django.contrib import admin
from core.models import CheckIn, IssueDetail, Person

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


class CheckInAdmin(admin.ModelAdmin):
    list_display = ['person',
                    'issue',
                    'time_spent',
                    'created_at',
                    'updated_at',
                    'description']


class  IssueDetailAdmin(admin.ModelAdmin):
    list_display = ["title", "issue_url"]

admin.site.register(Person, EmployeeAdmin)
admin.site.register(CheckIn, CheckInAdmin)
admin.site.register(IssueDetail, IssueDetailAdmin)
