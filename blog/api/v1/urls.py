from django.urls import path, include

# from some_app.views import AboutView
from . import views
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"post", views.PostViewSet, basename="post")
router.register(r"category", views.CategoryViewSet, basename="category")


app_name = "api-v1"
urlpatterns = [
    # path('post/', views.api_post_list,name= 'api_post_list'),
    # path('post/', views.PostList.as_view(), name='api_post_list'),
    # path('post/<int:pk>/', views.PostDetail.as_view(), name='api_post_detail'),
    # path('post/', views.PostViewSet.as_view({'get':'list'}),name= 'post_api_set'),
    # path('post/<int:pk>/', views.PostViewSet.as_view({'get': 'retrieve','put':'update','delete':'destroy'}), name='post_detail_api_set'),
    path("", include(router.urls)),
]
