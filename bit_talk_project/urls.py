from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
# from bit_talk_app_main import views, open_apis
from bit_talk_app_course.views import CoursesViewSet
from bit_talk_app_news.views import NewsViewSet, NewsFeedViewSet
from bit_talk_misc_api.views import (
    ModerationKeywordViewSet,
    StaticContentViewSet,
    ContactUsViewSet,
    CategoriesViewSet,
    LanguagesViewSet,
    BannersViewSet
    )
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    )
from bit_talk_posts.views import PostsViewSet
from rest_framework import routers
from bit_talk_cmc.views import CmcCoinsViewSet, CoinsViewSet
from bit_talk_root.views import MongoUserViewSet
# from bit_talk_root.views import CustomObtainTokenPairView as MongoTPV

router = routers.DefaultRouter()
router.register('courses', CoursesViewSet, 'courses')
router.register('news', NewsViewSet, 'news')
router.register('static-content', StaticContentViewSet, 'static-content')
router.register('contactus', ContactUsViewSet, 'contactus')
router.register('categories', CategoriesViewSet, 'categories')
router.register('cmc-coins', CmcCoinsViewSet, 'cmc-coins')
router.register('coins', CoinsViewSet, 'coins')
router.register('languages', LanguagesViewSet, 'languages')
router.register('newsfeed', NewsFeedViewSet, 'newsfeed')
router.register('banners', BannersViewSet, 'banners')
router.register('users', MongoUserViewSet, 'users')
router.register('posts', PostsViewSet, 'posts')
router.register('moderation-keywords', ModerationKeywordViewSet, 'ModerationKeywordsAPI')


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('users_profile/', include('bit_talk_app_main.urls')),
    path('openapi/', get_schema_view(
        title="Bit talk API Service",
        description="Frontend developers hoping to use our service"
    ), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='documentation.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

    # path('accounts/', include('django.contrib.auth.urls')),
    # path('news/', include('bit_talk_app_news.urls')),
    path('misc/', include('bit_talk_misc_api.urls')),

    # Api's related to Coins
    # path('coins', views.CoinsList.as_view()),
    # path('coins/<int:pk>/', views.CoinsDetail.as_view()),

    # path('newsfeed', views.NewsFeedList.as_view()),
    # path('newsfeed/<int:pk>/', views.NewsFeedDetail.as_view()),

    # Open API's
    # path('hello_world/', open_apis.hello_world),
    # path('coins/list/', open_apis.get_coins_list),
    # path('coins/latest/', open_apis.get_coins_latest),
    # path('v1/coins/ohlcv/historic/', open_apis.get_coins_ohlcv_historic),

    # APi's related to User Management
    # path('register/', views.RegisterView.as_view(), name='auth_register'),

    # temporarily commenting change pwd and reset pwd - Dont delete
    # path('change_password/<int:id>', views.ChangePasswordView.as_view(), name='auth_change_pwd'), # noqa
    # path('pwd_reset/', views.password_reset_request),

    # path('login/', views.CustomObtainTokenPairView.as_view(), name='token_obtain_pair'), # noqa
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # noqa
    # path('login/token/verify/', TokenVerifyView.as_view(), name='token_verify'), # noqa
    # path('logout/', views.user_logout),
    # path('users/', include('bit_talk_app_main.urls')) # commenting existing user table
]
urlpatterns = urlpatterns + router.urls
