from django.urls import path, include

# from some_app.views import AboutView
from . import views
from django.views.generic import TemplateView

app_name = "blog"
urlpatterns = [
    # path("", views.IndexView.as_view(), name="index"),
    # path("post/", views.PostListView.as_view(), name="post_list"),
    # path("detail/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    # path("post/create/", views.PostCreateView.as_view(), name="post_create"),
    # path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
    # path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path("api/v1/", include("blog.api.v1.urls")),
]
