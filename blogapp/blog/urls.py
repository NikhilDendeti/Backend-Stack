
from django.urls import path
from .views import RegisterUser,LoginUser,LogoutUser,CreatePost,CommentDetailView,CommentCreateView,PostDetailView


urlpatterns=[
    path('register/',RegisterUser.as_view(),name='register'),
    path('login/',LoginUser.as_view(),name="login"),
    path('logout/',LogoutUser.as_view(),name="logout"),
    path('posts/', CreatePost.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    path('posts/<int:post_id>/comments/', CommentCreateView.as_view(), name='comment-list-create'),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),

]