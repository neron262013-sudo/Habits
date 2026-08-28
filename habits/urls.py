from rest_framework.routers import SimpleRouter

from habits.views import HabitViewSet
from habits.apps import HabitsConfig


app_name = HabitsConfig.name

router = SimpleRouter()
router.register("", HabitViewSet)

urlpatterns = router.urls