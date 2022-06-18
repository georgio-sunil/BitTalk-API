from django.urls import path
from bit_talk_misc_api import views

urlpatterns = [
    path('subscribe', views.SubscribeList.as_view()),
    path('unsubscribe/<str:email>/', views.SubscribeDetail.as_view()),
]
