from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('trip/<int:id>/view/', views.view_trip, name="view-trip"),
     path('dashboard', views.dashboard, name="dashboard"),
     path('add-to-cart/<int:trip_id>/', views.add_to_cart, name='add_to_cart'),
     path('cart/', views.cart_detail, name='cart_detail'),
     path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
     path('item/decrement/<int:trip_id>/', views.item_decrement, name='item_decrement'),
     path('item/increment/<int:trip_id>/', views.item_increment, name='item_increment'),
     path('register/', views.RegisterView.as_view(), name='register'),
     path('signout/', views.signout, name='signout'),
]

