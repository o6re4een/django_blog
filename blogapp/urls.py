from django.urls import path

from . import views

urlpatterns = [
    path("post/", views.index, name="index"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("post/create/", views.create_post, name="create_post"),
    path("register/", views.register, name="register"),
]
