from rest_framework import routers
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SignUp, CustomerDetails, SearchConnection


router = DefaultRouter()
router.register('customer', CustomerDetails, basename='CustomerDetails')
router.register('search_connection', SearchConnection, basename='search_connection')

urlpatterns = [
    path('sign_up/', SignUp.as_view()),
    # path('login/', LogIn.as_view()),
]
urlpatterns += router.urls
