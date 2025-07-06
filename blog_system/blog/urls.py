from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-post/', views.create_post, name='create_post'),
    path('posts/', views.get_posts, name='get_posts'),
    path('post/<int:post_id>/', views.get_post, name='get_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
]
