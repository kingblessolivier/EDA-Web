from django.urls import path
from. import views
from django.conf.urls import handler404, handler500
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
    path('terms-and-conditions/', views.terms_and_conditions, name='terms'),
    path('privacy-policy/', views.privacy_policy, name='privacy'),
    path('reset-password/', views.reset_password, name='reset_password'),

]

urlpatterns += [

    # Profile urls
    path('profile/', views.profile, name='profile'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/profile/', user_detail_view, name='user-detail'),
    path('users/add/', UserCreateView.as_view(), name='user-add'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('users/delete/<int:pk>/', delete_user, name='user-delete'),
    path('add-team-member/', add_team_member, name='add-team-member'),
    path('team-members/delete/<int:pk>/', delete_team_member, name='team-member-delete'),
    path('team-members/', TeamListView.as_view(), name='team-members'),
    path('customer_messages/', views.customer_messages, name='customer_messages'),
    path('delete_message/<int:pk>/', views.delete_message, name='delete_message'),
    path('add_message/', views.add_message, name='add_message'),
    path('add_gallery/', views.add_gallery, name='add_gallery'),
    path('delete_gallery/<int:pk>/', views.delete_gallery, name='delete_gallery'),
    path('gallery/', views.galleryView, name='gallery'),
    path('edit_gallery/<int:pk>/', views.edit_gallery, name='edit_gallery')
]

handler404 = views.custom_404_view
handler500 = views.custom_500_view