from django.urls import path
from . import views

urlpatterns = [
    path('create-company/', views.create_company, name='create_company'),
    path('post-job/', views.post_job, name='post_job'),
    path('jobs/', views.get_jobs, name='get_jobs'),
    path('apply/', views.apply_job, name='apply_job'),
    path('applicants/<int:job_id>/', views.get_applicants, name='get_applicants'),
]
