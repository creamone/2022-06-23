from rest_framework import serializers
from .models import Category, Item, Order, ItemOrder


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # 아이템에 카테고리 하나 Foreign Key One to many
    # category = serializers.SerializerMethodField()

    # 피자 {'name' : 'pizza'} -> pizza
    # 햄버거 ->hamburger
    # obj ; Item object
    # def get_category(self,obj):
    # name = obj.category.name
    # name = "dongwoo"
    # return name
    # obj.category: 피자, 햄버거, ..,
    # result : 'pizza', 'hamburger'
    class Meta:
        model = Item
        fields = ['name', 'category', 'image_url']

    def create(self, validated_data):
        # validated_data = {'name' : 'cheese pizza',
        #                     'category': {'name':'pizza'},...
        # }
        category_data = validated_data.pop('category')  # {'name': 'pizza'}
        category_name = category_data.get('name')  # 'pizza'
        category_object = Category.objects.get(
            name=category_name)  # 피자라는 이름을 가진 오브젝트

        print(validated_data)
        item = Item(category=category_object, **validated_data)
        item.save()

        return item


class OrderSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=True)  # 다대다

    class Meta:
        model = Order
        fields = ['delivery_address', 'order_date', 'item']


class ItemOrderSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    item = ItemSerializer()

    class Meta:
        model = Order
        fields = ['order', 'item', 'item_count']
