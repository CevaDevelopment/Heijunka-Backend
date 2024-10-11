from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import SiteViewSet, TypeClientViewSet, ClientViewSet, ScheduleViewSet, RegisterView, LoginView, UserViewSet, \
    TaskAssignmentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'sites', SiteViewSet)
router.register(r'type-clients', TypeClientViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'task-assignments', TaskAssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('auth/renew/', TokenRefreshView.as_view(), name='token_refresh'),
]
