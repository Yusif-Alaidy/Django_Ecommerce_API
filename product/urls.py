from django.urls   import path

from product import views

urlpatterns = [
    path('products/', views.get_all_products, name='products'),
    path('products/<int:pk>/', views.get_by_id_product, name='get_by_id_product'),
    path('products/new', views.new_product, name='new_product'),
]
