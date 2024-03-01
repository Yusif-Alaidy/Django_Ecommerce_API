from django.shortcuts           import get_object_or_404,render
from rest_framework.decorators  import api_view,permission_classes
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework             import status
from rest_framework.pagination  import PageNumberPagination
from django.db.models           import Avg

from product.filters           import *
from product.models            import *
from product.serializers       import *
# Create your views here.

@api_view(['GET'])
def get_all_products(request):
    products               = Product.objects.all()
    
    # This called model with filter 
    filterset              = ProductFilter(request.GET, queryset=products)
    
    ########## PAGINATOR ##########
    paginator              = PageNumberPagination()
    ### page_size
    paginator.page_size    = 2
    ### query_set
    queryset               = paginator.paginate_queryset(filterset.qs, request) 
    
    ########## SERIALIZER CONVERT DATABASE TO API ##########
    serializer             = ProductSerializer(products, many=True)
    ### This serialize with filter
    serializer_filter      = ProductSerializer(filterset.qs, many=True)
    ### This serialize pagination
    serializer_pagination  = ProductSerializer(queryset, many=True)
    
    context = {
        ###### RETURN ALL PRODUCT ######
        # "products":serializer.data,
        
        ###### return filter product ######
        "products":serializer_pagination.data,
        "products":serializer_pagination.data,
    }
    
    return Response(context)

@api_view(['GET'])
def get_by_id_product(request,pk):
    product    = get_object_or_404(Product, id=pk)
    # serializer convert Database to API
    serializer = ProductSerializer(product, many=False)
    context = {
        "products":serializer.data,
    }
    
    return Response(context)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data
    serializer = ProductSerializer(data = data)

    if serializer.is_valid():
        product = Product.objects.create(**data,user=request.user)
        res = ProductSerializer(product,many=False)

        return Response({"product":res.data})
    else:
        return Response(serializer.errors)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request,pk):
    product = get_object_or_404(Product,id=pk)

    if product.user != request.user:
        return Response({"error":"Sorry you can not update this product"}
                        , status=status.HTTP_403_FORBIDDEN)
    
    product.name = request.data['name']
    product.descriptions = request.data['descriptions']
    product.price = request.data['price']
    product.brand = request.data['brand']
    product.category = request.data['category']
    product.ratings = request.data['ratings']
    product.stock = request.data['stock']

    product.save()
    serializer = ProductSerializer(product,many=False)
    return Response({"product":serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request,pk):
    product = get_object_or_404(Product,id=pk)

    if product.user != request.user:
        return Response({"error":"Sorry you can not update this product"}
                        , status=status.HTTP_403_FORBIDDEN)
    
    product.delete()

    return Response({"Details":"Delete action is done"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request,pk):
    # user ==> user.token
    user    = request.user
    # product ==> product.id
    product = get_object_or_404(Product,id=pk)
    # data
    data    = request.data
    # connect user with product.review 
    review  = product.reviews.filter(user=user)
    # if user write a less for 0 or top for 5 
    if data['rating'] <= 0 or data['rating'] > 5:
        return Response({"error":'Please select between 1 to 5 only'}
                        ,status=status.HTTP_400_BAD_REQUEST) 
    elif review.exists():
        # convert old data to new data
        new_review      = {'rating':data['rating'], 'comment':data['comment'] }
        # update old data
        review.update(**new_review)
        # average of all rating from integer (0 to 5)
        rating          = product.reviews.aggregate(avg_ratings = Avg('rating'))
        # ratings in product model = rating
        product.ratings = rating['avg_ratings']
        # save
        product.save()

        return Response({'details':'Product review updated'})
    else:
        Review.objects.create(
            user=user,
            product=product,
            rating= data['rating'],
            comment= data['comment']
        )
        rating          = product.reviews.aggregate(avg_ratings = Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({'details':'Product review created'})
    


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request,pk):
    user    = request.user
    product = get_object_or_404(Product,id=pk)   
    review  = product.reviews.filter(user=user)


    if review.exists():
        review.delete()
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        if rating['avg_ratings'] is None:
            rating['avg_ratings'] = 0
            product.ratings = rating['avg_ratings']
            product.save()
            return Response({'details':'Product review deleted'})
    else:
        return Response({'error':'Review not found'},status=status.HTTP_404_NOT_FOUND)

