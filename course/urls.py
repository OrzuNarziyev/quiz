from django.urls import path
from . import views

from quiz import views as quiz_views

app_name = 'course'

urlpatterns = [

    path('', views.course_list_view, name='course_list'),

    path('categories/', views.course_home, name="course_home"),
    path('categories/<slug:slug>/', views.course_home, name="course_cat"),
    path('categories/<slug:parent_slug>/<slug:cat_slug>', views.user_course_list_view, name="course_category_list"),

    path('<slug:course_slug>/filter',
         views.course_list_view, name='course_filter'),
    path('create/', views.course_create_view, name='course_create'),
    path('detail/<slug:slug>/', views.course_detail_view, name='course_detail'),
    path('htmx/detail/<int:pk>/', views.course_include_detail_view, name='course_include_detail'),
    path('update/<int:pk>/', views.course_update_view, name='course_update'),
    path('active/<int:pk>', views.active_or_deactive_course, name='active_or_deactive_course'),
    path('delete/<int:pk>/', views.course_delete_view, name='course_delete'),

    # module
    path('module/<int:course_id>', views.module_form, name='module_create'),
    path('module/detail/<int:pk>', views.module_detail, name='module_detail'),
    path('module/<int:pk>/update', views.module_update_view, name="module_update"),
    path('module/<int:pk>/delete', views.module_delete_view, name="module_delete"),
    path('module/<int:module_id>/content/<model_name>/create', views.content_create_update_view,
         name="module_content_create"),
    path('module/<int:module_id>/content/<model_name>/<int:pk>/update', views.content_create_update_view,
         name="module_content_update"),
    path('module/<module_id>/<content_id>/detail/<item_id>/', views.content_detail_view, name='module_content_detail'),
    path('module/content/<int:pk>/delete', views.content_delete_view, name='module_content_delete'),

    # module quiz 
    path('module/<module_id>/create/quiz', views.module_create_quiz, name='module_quiz_create'),
    path('module/<module_id>/update/quiz/<quiz_id>', views.module_create_quiz, name='module_quiz_update'),
    path('module/<quiz_id>/detail/quiz/<module_id>', quiz_views.htmx_quiz_detail_view, name='module_quiz_detail'),

    # users paths

    path('user/detail/<int:pk>/', views.user_course_detail, name="user_course_detail"),
    path('user/courses', views.course_categories, name='user_course_list'),
    path('user/<slug:slug>', views.course_categories, name='user_course_categories'),
    path('user/module/detail/<int:pk>', views.module_detail_view, name='user_module_detail_view'),

    # fetch api

]
