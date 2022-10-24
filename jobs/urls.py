from django.urls import path
from jobs import views

urlpatterns = [
    path('jobs/', views.get_all_jobs, name='jobs'),
    path('jobs/<str:pk>/', views.get_job_by_id, name='job'),
    path('jobs/<str:pk>/update', views.update_job, name='update_job'),
    path('jobs/<str:pk>/delete', views.delete_job, name='delete_job'),
    path('jobs/add/', views.add_new_job, name='add_new_job'), 
    path('jobs/stats/<str:topic>/', views.get_topic_stats, name='get_topic_stats')
]