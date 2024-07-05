from rest_framework import status
from django.db.models import Sum
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from apistatisticapp.models import Event
from apistatisticapp.serializers import EventSerializer


class EventApiView(APIView):
    """
    GET - метод показа статистики /statistic/?from=2024-07-01&to=2024-07-04&ordering=-views.
    POST - метод сохранения статистики {"date": "2024-07-04", "views": "10", "clicks": "10", "cost": "0.1"}.
    DELETE - метод сброса статистики (удаляет всю сохраненную статистику).
    """

    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Метод показа статистики.
        Принимает на вход: from - дата начала периода (включительно), to - дата окончания периода (включительно).
        Отвечает статистикой, отсортированной по дате. В ответе должны быть поля: date, views, clicks, cost, а также
        cpc = cost/clicks (средняя стоимость клика) и
        cpm = cost/views * 1000 (средняя стоимость 1000 показов).
        """
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        reverse = False
        try:
            ordering = request.query_params.get('ordering')
            if ordering[0] == '-':
                reverse = True
                ordering = ordering[1:]
        except:
            ordering = 'date'

        if not from_date or not to_date:
            return Response({'error': 'Both "from" and "to" dates are required.'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Event.objects.filter(date__range=[from_date, to_date]).values('date').annotate(
            views=Sum('views'),
            clicks=Sum('clicks'),
            cost=Sum('cost')
        ).order_by('date')

        serializer = EventSerializer(queryset, many=True)
        serializer_data = sorted(serializer.data, key=lambda p: p[ordering], reverse=reverse)
        return Response(serializer_data)

    def post(self, request: Request) -> Response:
        """
        Метод сохранения статистики.
        Принимает на вход date, views, clicks, cost.
        Статистика агрегируется по дате.
        """
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request: Request) -> Response:
        """
        Метод сброса статистики
        Удаляет всю сохраненную статистику.
        """
        Event.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
