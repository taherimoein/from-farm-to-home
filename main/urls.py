from main import views
from django.urls import path

app_name = 'main'
urlpatterns = [
    path('', views.indexpage, name = 'indexpage'),
    path('cart/', views.cart, name = 'cart'),
    path('register/', views.register, name = 'register'),
    path('signin/', views.signin, name = 'signin'),
    path('account/', views.account, name = 'account'),
    path('signout/', views.signout, name = 'signout'),
    path('products/', views.products, name = 'products'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('products/<int:pk>/', views.product_page, name = 'product_page'),
]