from . import views
from rest_framework.routers import DefaultRouter

app_name = "api_v1"


router = DefaultRouter()
router.register("", views.TodoModelViewSet, basename="todo")
urlpatterns = router.urls
