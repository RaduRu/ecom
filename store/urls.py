from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.store, name= "store"),
    path('cart/', views.cart, name= "cart"),
    path('checkout/', views.checkout, name= "checkout"),
    path('category/', views.checkout, name= "category"),
    path('update_item/', views.updateItem, name= "update_item"),
    path('process_order/', views.processOrder, name= "process_order"),
    path('category/<str:foo>', views.category, name="category"),
    path('about/', views.about, name= "about"),
    path('login/', views.login_user, name= "login"),
    path('logout/', views.logout_user, name= "logout"),
    
]