from django.urls import path
from .views import *
from knox import views as knox_views

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('emailcheck/', EmailCheckView.as_view(), name='email_check'),
    path('user/<int:user_id>/', ResetPasswordView.as_view(), name='password_reset'),
    path('music/', MusicListView.as_view(), name='music'),
    path('music/favorites/', MusicFavouriteListView.as_view(), name='favorites'),
    path('music/popular', MusicPopularListView.as_view(), name='popular'),
    path('music/new', MusicNewListView.as_view(), name='new'),
    path('music/recom', MusicRecomenmendListView.as_view(), name='recom')
]
