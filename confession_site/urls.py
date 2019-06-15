from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'confession_site'
urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.result, name='result'),
    path('recall/', views.recall, name='recall'),
    path('error/', views.error, name='error'),
    path('delete/', views.delete, name='delete'),
    path('recall-index/', views.recall_index, name='recall-index'),
    path('about/', views.about, name='about'),
    path('manage/', views.manage, name='manage'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('edit_post/', views.edit_post, name='edit_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
