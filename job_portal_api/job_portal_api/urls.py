from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({"message": "Job Portal API is running!"})

urlpatterns = [
    path('', root_view),
    path('admin/', admin.site.urls),
    path('api/', include('jobs.urls')),
]
