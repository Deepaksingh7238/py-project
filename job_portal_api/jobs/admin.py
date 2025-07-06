from django.contrib import admin
from .models import Company, JobPost, Applicant

admin.site.register(Company)
admin.site.register(JobPost)
admin.site.register(Applicant)
