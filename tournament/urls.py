from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),
    path('participants/', views.participants, name='participants'),
    path('rating/', views.rating, name='rating'),
    path('games/', views.games, name='games'),
    #path('games/<game>/', views.games, name='game'),
    path('before_draw', views.before_draw, name='before_draw'),
    path('accounts/register/', views.account_register, name='account_register'),
    path('accounts/login/', views.account_login, name='account_login'),
    path('accounts/logout/', views.account_logout, name='account_logout'),
    path('accounts/me/', views.me, name='me'),
    path('accounts/me/<game>/', views.me, name='me_game'),
]
