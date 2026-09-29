from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [

    # Authentication
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path(
        'login/',
        LoginView.as_view(
            template_name='accounts/login.html'
        ),
        name='login'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Profile
    path(
        'profile/',
        views.ProfileView.as_view(),
        name='profile'
    ),
    path(
        'profile/edit/',
        views.ProfileUpdateView.as_view(),
        name='profile_edit'
    ),

    # Posts
    path(
        'posts/create/',
        views.PostCreateView.as_view(),
        name='post_create'
    ),
    path(
        'posts/',
        views.PostListView.as_view(),
        name='post_list'
    ),
    path(
        'posts/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/<int:pk>/edit/',
        views.PostUpdateView.as_view(),
        name='post_edit'
    ),
    path(
        'posts/<int:pk>/delete/',
        views.DeletePostView.as_view(),
        name='post_delete'
    ),

    # Comments
    path(
        'post/<int:pk>/add-comment/',
        views.add_comment,
        name='add_comment'
    ),
    path(
        'comment/<int:pk>/edit-comment/',
        views.CommentUpdateView.as_view(),
        name='edit_comment'
    ),
    path(
        'comment/<int:pk>/delete-comment/',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
    ),

    # Categories
    path(
        'categories/<int:pk>/',
        views.category_posts_view,
        name='category_posts'
    ),

    # My Posts
    path(
        'my-posts/',
        views.MyPostsView.as_view(),
        name='my_posts'
    ),

    # Search
    path(
        'search/',
        views.search_view,
        name='search'
    ),
]