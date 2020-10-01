from django.contrib import admin
from core.models import Person, CheckIn, IssueDetail
# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name','email')

class CheckInAdmin(admin.ModelAdmin):
    list_display = ['employee',
                    'issue',
                    'time_spent',
                    'created_at',
                    'updated_at',
                    'description']

admin.site.register(Person, EmployeeAdmin)
admin.site.register(CheckIn, CheckInAdmin)
admin.site.register(IssueDetail)