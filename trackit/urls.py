import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from core.views import EmployeeViewSet

router = routers.DefaultRouter()
router.register('employee', EmployeeViewSet, "employee")
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('__debug__/', include(debug_toolbar.urls)),
]