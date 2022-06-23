from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ItemSerializer,  OrderSerializer
from .models import Item, Category, Order
from .serializers import ItemSerializer


from django.db.models.query_utils import Q
from django.utils import timezone
from datetime import timedelta
# Create your views here.

# Item 기능


class ItemView(APIView):
    # Item 조회 기능

    def get(self, request):
        # category_name = appliance
        category_name = request.GET['category']  # appliance 스트링

        # category_object = {'name' : 'appliacne'}
        category_object = Category.objects.get(name=category_name)

        # item을 가져온다 item들이 가져오는건데  category_object 위에있는 category만같은 것만 가져온다
        # category_id = category_object.id db에 비교를 할수있다.
        items = Item.objects.filter(category=category_object)

        response = ItemSerializer(items, many=True)
        return Response(response.data)

    def post(self, request):
        data = request.data

        item_serializer = ItemSerializer(data=request.data)
        if item_serializer.is_valid():
            item_serializer.save()

            return Response({'message': "저장 완료!"}, status=status.HTTP_200_OK)

        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # item = Item.objects.create(**data)
        # item.save()

        # print(data)

        # return Response({})

# order 기능


class OrderView(APIView):
    # id로 order 조회 기능
    def get(self, request):
        order_id = request.GET['order_id']
        print(order_id)

        #조건 = query

        time = timezone.now() - timedelta(days=7)
        # time = timezone.now()

        query = Q(id=order_id) & Q(order_date__gte=time)

        order_object = Order.objects.get(query)
        return Response(OrderSerializer(order_object).data)
        # order_object = Order.objects.get(id=order_id)
        # order_object = Order.objects.get(query) 오브젝트값
        # order_objects = Order.objects.filter(query) 빈리스트 쿼리셋을 가져온다

        # orders = Order.objects.all() #오더를 다가져오는거 오브젝트
        # return Response(OrderSerializer, order_object)
