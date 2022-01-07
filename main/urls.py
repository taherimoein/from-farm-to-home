from main import views
from django.urls import path

app_name = 'main'
urlpatterns = [
    path('', views.indexpage, name = 'indexpage'),
    path('register/', views.register, name = 'register'),
    path('signin/', views.signin, name = 'signin'),
    path('signout/', views.signout, name = 'signout'),
]