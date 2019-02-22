from django.urls import path

from . import views

app_name = 'blogmanagement'
urlpatterns = [
    # path('fake_authors', views.generate_fake_authors, name='fake_authors'),
    path('fake_posts', views.generate_fake_posts, name='fake_posts'),
    path('fake_comments', views.generate_fake_comments, name='fake_comments'),

    path('', views.index, name='index'),
    path('authors/<slug:author_slug>/', views.posts_by_author, name='posts_by_author'),
    path('categories/<slug:category_slug>/', views.posts_by_category, name='posts_by_category'),


    path('manage/', views.manage_home, name='manage_home'),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

    path('manage/categories/', views.categories, name='categories'),
    path('manage/categories/new', views.new_category_view, name='new_category_view'),
    # path('categories/new_category', views.new_category, name='new_category'),

    # path('categories/<int:category_id>/edit', views.edit_category_view, name='edit_category_view'),
    path('manage/categories/<int:category_id>/edit', views.edit_category, name='edit_category'),

    path('manage/categories/<int:category_id>/delete_confirmation', views.category_delete_confirmation_view,
         name='delete_category'),

    path('manage/status/', views.status, name='status'),
    path('manage/status/new', views.new_status_view, name='new_status_view'),
    path('manage/status/<int:status_id>/edit', views.edit_status_view, name='edit_status'),
    path('manage/status/<int:status_id>/delete_confirmation',
         views.status_delete_confirmation_view, name='delete_status'),
    path('manage/status/<slug:status_slug>/', views.posts_by_status, name='posts_by_status'),

    path('manage/authors/', views.authors, name='authors'),
    path('manage/authors/new', views.new_author_view, name='new_author_view'),
    path('manage/authors/<int:author_id>/edit', views.edit_author_view, name='edit_author'),
    path('manage/authors/<int:author_id>/delete_confirmation',
         views.author_delete_confirmation_view, name='delete_author'),

    path('manage/posts/', views.posts, name='posts'),
    path('posts/<slug:post_slug>/', views.post_detail_view, name='post_detail'),
    path('manage/posts/new', views.new_post_view, name='new_post_view'),
    path('manage/posts/<int:post_id>/edit', views.edit_post_view, name='edit_post'),
    path('manage/posts/<int:post_id>/delete_confirmation', views.post_delete_confirmation_view, name='delete_post'),
    path('manage/posts/<int:post_id>/publish', views.publish_post, name='publish_post'),
    path('comment', views.save_comment, name='save_comment'),
]