from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('manage/'),
    path('quiz/', views.quiz_home, name="quiz_home"),
    path('quiz/<slug:slug>/', views.quiz_home, name="quiz_cat"),

    path('quiz/detail/<int:pk>/', views.user_quiz_detail, name="user_quiz_detail"),
    path('quiz/<int:pk>/start/', views.quiz_start, name="user_quiz_start"),
    path('quiz/<int:pk>/start/data', views.quiz_data_view, name="quiz_data"),
    path('quiz/<int:pk>/start/save', views.quiz_save, name="quiz_save"),
    path('quiz/<int:pk>/start/fetch', views.FetchApiView.as_view(), name="fetch"),
    # path('quiz/<int:pk>/save/', views.quiz_start, name="user_quiz_save"),

    path('quiz/create', views.quiz_create_view, name='quiz_create_view'),
    path('quiz_list/', views.quiz_list_view, name='quiz_list'),
    path('quiz/<int:pk>', views.quiz_detail_view, name='quiz_detail'),

    # htmx urls
    path('htmx/quiz/<int:pk>', views.htmx_quiz_detail_view, name='htmx_quiz_detail'),
    path('htmx/quiz/<int:pk>/delete', views.quiz_delete_view, name='quiz_delete'),
    path('htmx/quiz/<int:pk>/update', views.update_quiz, name='quiz_update'),
    path('htmx/create/question/<quiz_id>', views.question_form, name='create_question'),
    path('htmx/create/question/exel/<quiz_id>', views.export_question_excel, name='create_question_with_excel'),
    path('update/question/<question_id>', views.update_question, name='update_question'),
    path('delete/question/<question_id>', views.delete_question, name='delete_question'),

    # manage
    path('manage/dashboard', views.manage_dashboard, name='manage_dashboard')
]
