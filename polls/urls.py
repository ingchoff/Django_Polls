from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('detail/<int:poll_id>/', views.detail, name='poll_detail'),
    path('create/', views.create, name='create_poll'),
    path('create-comments/', views.comment, name='create_comment'),
    path('create-question/', views.question, name='create_question'),
    path('login/', views.my_login, name='my_login'),
    path('logout/', views.my_logout, name='my_logout'),
    path('change-pass/', views.my_change_pass, name='my_change'),
    path('update/<int:poll_id>/', views.update, name='update_poll')
]
