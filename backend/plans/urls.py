from rest_framework import routers

from plans.views import PlanViewSet

router = routers.DefaultRouter()
router.register(r'plans', PlanViewSet, base_name='plan')

urlpatterns = router.urls