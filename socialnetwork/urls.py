from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('customer', views.CustomerDetails, basename='CustomerDetails')
router.register('search_connection', views.SearchConnection, basename='search_connection')
router.register('connection_request_status', views.PendingRequest, basename='pending_request')
router.register('friends', views.FriendsList, basename='friends')

urlpatterns = [
    path('sign_up/', views.SignUp.as_view()),
    path('send_connection_request/', views.SendConnectionRequest.as_view()),
    path('process_request/', views.ProcessRequest.as_view())
    # path('login/', LogIn.as_view()),
]
urlpatterns += router.urls
