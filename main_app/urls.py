from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('dragons/', views.dragons_index, name='dragons_index'),
    path('dragons/<int:dragon_id>/', views.dragons_detail, name='dragons_detail'),
    path('dragons/create/', views.DragonCreate.as_view(), name='dragons_create'),
    path('dragons/<int:pk>/update', views.DragonUpdate.as_view(), name='dragons_update'),
    path('dragons/<int:pk>/delete', views.DragonDelete.as_view(), name='dragons_delete'),
    path('toys/', views.toys_index, name='toys_index'),
    path('toys/<int:toy_id>/', views.toys_detail, name='toys_detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update', views.ToyUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete', views.ToyDelete.as_view(), name='toys_delete')
]