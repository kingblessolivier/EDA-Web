from django.urls import path
from. import views
from .views import training_detail
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('partners/',views.partners, name='partners'),
    path('trainings/', views.training_list, name='trainings'),
    path('trainings/add/', views.add_training, name='add_training'),
    path('trainings/update/<int:pk>/', views.edit_training, name='update_training'),
    path('trainings/delete/<int:pk>/', views.delete_training, name='delete_training'),
    path('training/<int:training_id>/', training_detail, name='training_detail'),
    path('partners/add/', add_partner, name='add_partner'),
    path('partners/edit/<int:partner_id>/', edit_partner, name='edit_partner'),
    path('partners/delete/<int:partner_id>/', delete_partner, name='delete_partner'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('projects/', views.project_list, name='projects'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/add/', views.add_project, name='add_project'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('project/<int:pk>/update/', views.edit_project, name='edit_project'),


]