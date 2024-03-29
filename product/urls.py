from django.urls   import path

from product import views

urlpatterns = [
    path('products/',                 views.get_all_products,  name= 'products'),
    path('products/<int:pk>/',        views.get_by_id_product, name= 'get_by_id_product'),
    path('products/new/',             views.new_product,       name= 'new_product'),
    path('products/update/<int:pk>/', views.update_product,    name= 'update_product'),
    path('products/delete/<int:pk>/', views.delete_product,    name= 'delete_product'),
    path('reviews/<int:pk>/',         views.create_review,     name= 'create_review'),
    path('reviews/delete/<int:pk>/',  views.delete_review,     name= 'delete_review'),
]
