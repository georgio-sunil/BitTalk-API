# from django.urls import path
# from bit_talk_cmc.views import CmcCoinsViewSet

# # snippet_list = CmcCoinsViewSet.as_view({
# #     'get': 'list',
# #     'post': 'create'
# # })
# # snippet_detail = CmcCoinsViewSet.as_view({
# #     'get': 'retrieve',
# #     'put': 'update',
# #     'patch': 'partial_update',
# #     'delete': 'destroy'
# # })

# <URLPattern '^courses/$' [name='courses-list']>
# <URLPattern '^courses\.(?P<format>[a-z0-9]+)/?$' [name='courses-list']>
# <URLPattern '^courses/(?P<id>[^/.]+)/$' [name='courses-detail']>
# <URLPattern '^courses/(?P<id>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='courses-detail']>

# # urlpatterns = [
# #     # path('NewsAPI/', views.NewsViewSet.as_view()),
# #     # path('<str:_id>/', views.NewsDetail.as_view()),
# #     # path('cmc-fetch-coins', views.get_news_btc),
# #     path('coins/', snippet_list, name='snippet-list'),
# #     path('coins/<int:_id>/', snippet_detail, name='snippet-detail'),
# # ]

