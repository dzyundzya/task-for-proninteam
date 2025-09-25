from rest_framework.routers import DefaultRouter

from server.apps.collects.views import CollectViewSet

router = DefaultRouter()
router.register(r'collects', CollectViewSet, basename='collects')


urlpatterns = router.urls
