from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('manage/'),
    path('testlar/', views.quiz_home, name="quiz_home"),
    path('test/<slug:slug>/', views.quiz_home, name="quiz_cat"),
    path('test/user/statistics', views.ResultApiView.as_view(), name='statistics_user'),
    path('test/<slug:slug>/<slug:quiz_slug>', views.user_quiz_list_view, name="user_quiz_list_view"),

    path('test/detail/<int:pk>/', views.user_quiz_detail, name="user_quiz_detail"),
    path('test/<int:pk>/start/', views.quiz_start, name="user_quiz_start"),
    path('test/<int:pk>/start/data', views.quiz_data_view, name="quiz_data"),
    path('test/<int:pk>/start/save', views.quiz_save, name="quiz_save"),
    path('test/<int:pk>/start/fetch', views.FetchApiView.as_view(), name="fetch"),
    # path('test/<int:pk>/save/', views.quiz_start, name="user_quiz_save"),

    path('test/create', views.quiz_create_view, name='quiz_create_view'),
    path('quiz_list/', views.quiz_list_view, name='quiz_list'),
    path('test/<int:pk>', views.quiz_detail_view, name='quiz_detail'),

    # htmx urls
    path('htmx/test/<int:pk>', views.htmx_quiz_detail_view, name='htmx_quiz_detail'),
    path('htmx/test/<int:pk>/delete', views.quiz_delete_view, name='quiz_delete'),
    path('htmx/test/<int:pk>/update', views.update_quiz, name='quiz_update'),
    path('htmx/test/<int:pk>/active', views.active_or_deactive, name='quiz_active_or_deactive'),
    path('htmx/create/question/<quiz_id>', views.question_form, name='create_question'),
    path('htmx/create/question/exel/<quiz_id>', views.export_question_excel, name='create_question_with_excel'),
    path('update/question/<question_id>', views.update_question, name='update_question'),
    path('delete/question/<question_id>', views.delete_question, name='delete_question'),

    # statistics user
    # manage
    path('manage/', views.manage_dashboard, name='manage_dashboard'),
    path('manage/statistics', views.statistics, name='manage_statistics'),
    path('manage/employers', views.employers, name='manage_employers'),
    path('manage/organization', views.organizations, name='manage_organizations'),
    path('api/manage/dashboard/info', views.quiz_dashboard_info, name='api_dashboard_info'),
    path('api/manage/statistics/org', views.statistics_org_api, name='statistics_org_api'),

]
