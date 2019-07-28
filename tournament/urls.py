from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('success', views.success, name='success'),
    path('failure', views.failure, name='failure'),
    path('participants', views.participants, name='participants'),
    path('rating', views.rating, name='rating'),
    path('games', views.games, name='games'),
    path('games/<game>', views.games, name='game'),
    path('before_draw', views.before_draw, name='before_draw'),
]
