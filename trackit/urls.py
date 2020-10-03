from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from core.views import CheckInViewSet, IssueDetailViewSet, PersonViewSet

router = routers.DefaultRouter()
router.register('person', PersonViewSet, "person")
router.register('issues', IssueDetailViewSet, "issues")
router.register('checkin', CheckInViewSet, "checkin")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
