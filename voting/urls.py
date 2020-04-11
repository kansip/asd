"""voting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from voting_app import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('register/', views.register_view),
    # Список всех голосований
    path('votes/', views.votes_view),

    # Страница голосования
    path('vote/<int:vote_id>', views.vote_view),

    # История голосований
    path('votes/my', views.user_votes_view),

    # Редактор голосований
    path('votes/editor/', views.votes_editor_view),

    # Получение информации о голосовании
    path('vote/get/<int:vote_id>', views.get_vote_view),

    # Создать голосование
    path('vote/create/', views.vote_create_view),

    # Редактировать голосование
    path('vote/edit/<int:vote_id>', views.vote_edit_view),

    # Удаление голосование
    path('vote/delete/<int:vote_id>', views.vote_delete_view),

    # Страница профиля
    path('user/<int:user_id>', views.user_page_view),



]
