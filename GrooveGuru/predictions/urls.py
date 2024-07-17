# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('genre_classification/', views.genre_classification, name='genre_classification'),
    path('genre_recommendation/', views.genre_recommendation, name='genre_recommendation'),
    path('about/', views.about, name='about'),
    path('statistics/', views.statistics, name='statistics'),
    path('get_started/', views.get_started, name='get_started'),
    path('upload_audio/', views.upload_audio, name='upload_audio'),  # Add this line
    path('upload_audio/recommend_songs/<str:genre>/', views.recommend_songs, name='recommend_songs'),
]
