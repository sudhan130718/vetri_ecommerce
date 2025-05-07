from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    # path('', views.test, name='test'),
    path('test/', views.test, name='test'),
    path('home/', views.combined_view, name='home'),
    # path('products/', views.product_list, name='product_list'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
# product
    path('', views.product_list_new, name='product_list1'),
    path('list1', views.product_list_new, name='product_list1'),
    path('list', views.product_list, name='product_list'),
    path('products', views.products, name='products'),

    
    path('create/', views.product_create, name='product_create'),
    path('update/<int:pk>/', views.product_update, name='product_update'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

# cart
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-quantity/<int:item_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('remove-item/<int:item_id>/', views.remove_item, name='remove_item'),

    # checkout 
    path('checkout/', views.checkout, name='checkout'),

    # order
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),

]