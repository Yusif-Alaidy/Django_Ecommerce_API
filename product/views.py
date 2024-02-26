from django.shortcuts                   import render, get_object_or_404
from rest_framework.decorators          import api_view, permission_classes
from rest_framework.response            import Response
from rest_framework.pagination          import PageNumberPagination
from rest_framework.permissions         import IsAuthenticated


from product.filters                    import *
from product.models                     import *
from product.serializers                import *
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
    data       = request.data 
    serializer = ProductSerializer(data=data)
    
    if serializer.is_valid():
        product = Product.objects.create(**data, user=request.user)
        res = ProductSerializer(product, many=False)
        
        return Response({"product":res.data})
    else:
        return Response(serializer.errors)
    
    