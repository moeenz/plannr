import calendar
import datetime as dt

from rest_framework.response import Response
from rest_framework import viewsets, permissions, status

from plans.models import Plan
from plans.serializers import PlanSerializer


class PlanViewSet(viewsets.ViewSet):
    """ViewSet generic API for actions corresponding
    to Plan objects. `Much like serializer module, we can't use
    ModelViewSet due to incompatibility.`
    """

    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        try:
            year = int(request.GET.get('year', None))
            month = int(request.GET.get('month', None))
            month_start, month_end = calendar.monthrange(year, month)
            # Filter plans hapenning in the requested year, month for user.
            queryset = Plan.objects.filter(
                owner_id=request.user.id,
                start__gt=dt.datetime(year, month, month_start),
                end__lt=dt.datetime(year, month, month_end)
            )
            serializer = self.serializer_class(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
