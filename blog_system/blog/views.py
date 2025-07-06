from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
import json
from .models import Post, Comment

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({'success': False, 'error': 'Username already exists'}, status=400)
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({'success': False, 'error': 'Email already exists'}, status=400)
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return JsonResponse({'success': True, 'user_id': user.id, 'message': 'User registered successfully'})
    except KeyError as e:
        return JsonResponse({'success': False, 'error': f'Missing required field: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'user_id': user.id, 'username': user.username, 'message': 'Login successful'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)
    except KeyError as e:
        return JsonResponse({'success': False, 'error': f'Missing required field: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def create_post(request):
    try:
        data = json.loads(request.body)
        post = Post.objects.create(
            author=request.user,
            title=data['title'],
            content=data['content']
        )
        return JsonResponse({'success': True, 'post_id': post.id, 'message': 'Post created successfully'})
    except KeyError as e:
        return JsonResponse({'success': False, 'error': f'Missing required field: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_posts(request):
    try:
        page = request.GET.get('page', 1)
        posts = Post.objects.select_related('author').all()
        paginator = Paginator(posts, 10)
        posts_page = paginator.get_page(page)
        posts_data = []
        for post in posts_page:
            posts_data.append({
                'id': post.id,
                'title': post.title,
                'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
                'author': post.author.username,
                'created_at': post.created_at.isoformat(),
                'comments_count': post.comments.count()
            })
        return JsonResponse({
            'success': True,
            'posts': posts_data,
            'pagination': {
                'current_page': posts_page.number,
                'total_pages': paginator.num_pages,
                'has_next': posts_page.has_next(),
                'has_previous': posts_page.has_previous()
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_post(request, post_id):
    try:
        post = Post.objects.select_related('author').get(id=post_id)
        comments = Comment.objects.select_related('user').filter(post=post)
        comments_data = []
        for comment in comments:
            comments_data.append({
                'id': comment.id,
                'text': comment.text,
                'user': comment.user.username,
                'created_at': comment.created_at.isoformat()
            })
        return JsonResponse({
            'success': True,
            'post': {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author': post.author.username,
                'created_at': post.created_at.isoformat()
            },
            'comments': comments_data
        })
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Post not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def add_comment(request, post_id):
    try:
        data = json.loads(request.body)
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(
            post=post,
            user=request.user,
            text=data['text']
        )
        return JsonResponse({'success': True, 'comment_id': comment.id, 'message': 'Comment added successfully'})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Post not found'}, status=404)
    except KeyError as e:
        return JsonResponse({'success': False, 'error': f'Missing required field: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def logout_view(request):
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logged out successfully'})
