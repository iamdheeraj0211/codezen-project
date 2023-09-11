from django.urls import path
from .views import ProductListCreateView,ProductRetrieveUpdateDestroyView,OrdersListCreateView,RegisterUserView,OrdersRetriveUpdatedeleteView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns=[
    path('product/',ProductListCreateView.as_view()),
    path('product/<int:pk>/',ProductRetrieveUpdateDestroyView.as_view()),

    path('cu-order/',OrdersListCreateView.as_view()),
    path('cu-order/<int:pk>/',OrdersRetriveUpdatedeleteView.as_view()),

    path('register/',RegisterUserView.as_view()),
    path('login/',obtain_auth_token)
             ]