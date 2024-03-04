from django.shortcuts           import get_object_or_404
from rest_framework.decorators  import api_view,permission_classes
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from rest_framework             import status

from product.models             import Product   
from .serializers               import OrderSerializer
from .models                    import Order,OrderItem


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    user        = request.user 
    data        = request.data
    order_items = data['order_Items']

    if order_items and len(order_items) == 0:
        return Response({'error': 'No order recieved'},status=status.HTTP_400_BAD_REQUEST)
    else:
        total_amount = sum( item['price']* item['quantity'] for item in order_items)
        order        = Order.objects.create(
            user         = user,
            city         = data['city'],
            zip_code     = data['zip_code'],
            street       = data['street'],
            phone_no     = data['phone_no'],
            country      = data['country'],
            total_amount = total_amount,
        )
        for i in order_items:
            product = Product.objects.get(id=i['product'])
            item    = OrderItem.objects.create(
                product     = product,
                order       = order,
                name        = product.name,
                quantity    = i['quantity'],
                price       = i['price']
            )
            product.stock  -= item.quantity
            product.save()
        serializer = OrderSerializer(order,many=False)
        return Response(serializer.data)