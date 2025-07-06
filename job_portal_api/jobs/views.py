from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
import json
from .models import Company, JobPost, Applicant

@csrf_exempt
@require_http_methods(["POST"])
def create_company(request):
    try:
        data = json.loads(request.body)
        company = Company.objects.create(
            name=data['name'],
            location=data['location'],
            description=data['description']
        )
        return JsonResponse({
            'success': True,
            'company_id': company.id,
            'message': 'Company created successfully'
        })
    except KeyError as e:
        return JsonResponse({
            'success': False,
            'error': f'Missing required field: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def post_job(request):
    try:
        data = json.loads(request.body)
        company = Company.objects.get(id=data['company_id'])
        job = JobPost.objects.create(
            company=company,
            title=data['title'],
            description=data['description'],
            salary=data['salary'],
            location=data['location']
        )
        return JsonResponse({
            'success': True,
            'job_id': job.id,
            'message': 'Job posted successfully'
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Company not found'
        }, status=404)
    except KeyError as e:
        return JsonResponse({
            'success': False,
            'error': f'Missing required field: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_jobs(request):
    try:
        jobs = JobPost.objects.select_related('company').all()
        jobs_data = []
        for job in jobs:
            jobs_data.append({
                'id': job.id,
                'title': job.title,
                'description': job.description,
                'salary': job.salary,
                'location': job.location,
                'company_name': job.company.name,
                'company_location': job.company.location,
                'created_at': job.created_at.isoformat()
            })
        return JsonResponse({
            'success': True,
            'jobs': jobs_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def apply_job(request):
    try:
        data = json.loads(request.body)
        job = JobPost.objects.get(id=data['job_id'])
        applicant = Applicant.objects.create(
            name=data['name'],
            email=data['email'],
            resume_link=data['resume_link'],
            job=job
        )
        return JsonResponse({
            'success': True,
            'applicant_id': applicant.id,
            'message': 'Application submitted successfully'
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Job not found'
        }, status=404)
    except KeyError as e:
        return JsonResponse({
            'success': False,
            'error': f'Missing required field: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_applicants(request, job_id):
    try:
        job = JobPost.objects.get(id=job_id)
        applicants = Applicant.objects.filter(job=job)
        applicants_data = []
        for applicant in applicants:
            applicants_data.append({
                'id': applicant.id,
                'name': applicant.name,
                'email': applicant.email,
                'resume_link': applicant.resume_link,
                'applied_at': applicant.applied_at.isoformat()
            })
        return JsonResponse({
            'success': True,
            'job_title': job.title,
            'applicants': applicants_data
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Job not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
