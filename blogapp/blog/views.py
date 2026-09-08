from django.http import request
from os import name
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.contrib.auth import login,logout,authenticate
from django.utils.decorators import method_decorator
from django.views import View
from .models import User,Post,Category,Comment
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

# Create your views here.
@method_decorator(csrf_exempt,name='dispatch')
class RegisterUser(View):
    def post(self,request):
        try:
            data=json.loads(request.body)
        except:
            return JsonResponse({'error':'Invalid JSON body'},status=400)
        username=data.get('username')
        email=data.get('email')
        password=data.get('password')

        if not username or not password:
            return JsonResponse({'error':'username and passoword are required'},status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error':'useralready exist'})
        user=User.objects.create_user(username=username,email=email,password=password)
        return JsonResponse({'message':'user created successfully','username':user.username},status=201)

@method_decorator(csrf_exempt,name='dispatch')
class LoginUser(View):
    def post(self,request):
        try:
            data=json.loads(request.body)
        except:
            return JsonResponse({'error':'Invalid json body'},status=400)

        username=data.get('username')
        password=data.get('password')

        if not username or not password:
            return JsonResponse({'error':'username and password are required'},status=400)
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return JsonResponse({'message':'user logged in successfully','username':user.username},status=200)
        else:
            return JsonResponse({'error':'invalid credentials'},status=401)
    

@method_decorator(csrf_exempt,name='dispatch')
class LogoutUser(View):
    def post(self,request):
        logout(request)
        return JsonResponse({'message':'user logged out successfully'},status=200)

@method_decorator(csrf_exempt,name='dispatch')
class CreatePost(View):
    def get(self,request):
        posts=Post.objects.all()
        data=[
            {
                'id':post.id,
                'title':post.title,
                'author':post.author.username if post.author else None,
                'body':post.body,
                'category':list(post.category.values_list('name',flat=True)),
                'views':post.views,
                'status':post.status,
            }
            for post in posts
        ]
        return JsonResponse(data,safe=False)
    def post(self,request):
        if not request.user.is_authenticated:
            return JsonResponse({'error':'Login required'},status=401)
        try:
            data=json.loads(request.body)
        except:
            return JsonResponse({'error':'Invalid json body'},status=400)
        title=data.get('title')
        body=data.get('body')

        if not title:
            return JsonResponse({'Error':'Title is required'},status=400)
        if not body:
            return JsonResponse({'Error':'Body is required'},status=400)

        post=Post.objects.create(title=title,body=body,author=request.user)
        return JsonResponse({'message':'post created successfully'},status=201)

@method_decorator(csrf_exempt,name='dispatch')
class PostDetailView(View):
    def get(self,request,pk):
        post=get_object_or_404(Post,pk=pk)
        return JsonResponse({
            'id':post.id,
            'title':post.title,
            'author':post.author.username if post.author else None,
            'body':post.body,
            'category':list(post.category.values_list('name',flat=True)),
            'views':post.views,
            'status':post.status,
        })

    def put(self,request,pk):
        post=get_object_or_404(Post,pk=pk)
        if not request.user.is_authenticated:
            return JsonResponse({'error':'Login required'},status=401)
        if post.author != request.user:
            return JsonResponse({'error':'Not allowed'},status=403)

        try:
            data=json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error':'Invalid JSON body'},status=400)

        post.title=data.get('title',post.title)
        post.body=data.get('body',post.body)
        post.status=data.get('status',post.status)
        post.save()
        return JsonResponse({'message':'Post updated','id':post.id})

    def delete(self,request,pk):
        post=get_object_or_404(Post,pk=pk)
        if not request.user.is_authenticated:
            return JsonResponse({'error':'Login required'},status=401)
        if post.author != request.user:
            return JsonResponse({'error':'Not allowed'},status=403)

        post.delete()
        return JsonResponse({'message':'Post deleted'})

@method_decorator(csrf_exempt,name='dispatch')
class CommentCreateView(View):
    def get(self,request,post_id):
        post=get_object_or_404(Post,pk=post_id)
        comments=post.comments.all()
        data=[
            {
                'id':comment.id,
                'author':comment.author.username,
                'body':comment.body,
                'created_at':comment.created_at
            }
            for comment in comments
        ]
        return JsonResponse(data,safe=False)

    def post(self,request,post_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Login required'}, status=401)

        post = get_object_or_404(Post, pk=post_id)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)

        body = data.get('body')
        if not body:
            return JsonResponse({'error': 'body is required'}, status=400)

        comment = Comment.objects.create(post=post, author=request.user, body=body)
        return JsonResponse({'id': comment.id, 'body': comment.body}, status=201)   
        
@method_decorator(csrf_exempt,name='dispatch')
class CommentDetailView(View):
    def put(self,request,post_id,pk):
        if not request.user.is_authenticated:
            return JsonResponse({'error':'Login required'},status=401)
        comment=get_object_or_404(Comment,pk=pk,post_id=post_id)
        if comment.author != request.user:
            return JsonResponse({'error': 'Not Allowed'},status=403)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)
        comment.body=data.get('body',comment.body)
        comment.save()
        return JsonResponse({'message': 'Comments updated successfully!!','id':comment.id})


    def delete(self, request, post_id, pk):
        comment = get_object_or_404(Comment, pk=pk, post_id=post_id)
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Login required'}, status=401)
        if comment.author != request.user:
            return JsonResponse({'error': 'Not allowed'}, status=403)

        comment.delete()
        return JsonResponse({'message': 'Comment deleted'})