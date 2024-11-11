from lib2to3.fixes.fix_input import context

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from django.shortcuts import render , get_object_or_404
from django.template.context_processors import request

from .forms import CommentForm
from  .models import Post
from django.views import View

# all_posts = [
#
# ]
# Create your views here.

class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']

    context_object_name = 'posts'

    def get_queryset(self): #특정 조건에 맞는 객체만 조회하기
        queryset = super().get_queryset() #super를 통해 get_queryset() 메서드를 호출하여 기본 쿼리셋을 가져옵
        data = queryset[:3]
        return data


# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     #sorted_posts = sorted(all_posts, key=get_date) # 단순히 sort 사용하면 분류된 새로운 배열이 생성되므로 sorted 사용해야함
#     #latest_posts = sorted_posts[-3:] #끝에서 3번째 사용 , :-3은 끝에서 3개 제외한 나머지 반환
#     return render(request, "blog/index.html", {
#       "posts": latest_posts
#     })

class AllPostsView(ListView):
    template_name = 'blog/all-posts.html'
    context_object_name = 'posts'
    model = Post
    ordering = ['-date']
    context_object_name = 'all_posts'




# def posts(request):
#     return render(request, "blog/all-posts.html", {
#       "all_posts": Post.objects.all().order_by("-date")
#     })

class SinglePostView(View):
    def is_stored_post(self, request, post_id):  #나중에 볼 포스트 목록에 있는지 여부 확인
        stored_post = request.session.get("stored_post")

        if stored_post is not None:
            is_saved_for_later = post_id in stored_post
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)


        context = {
            'post': post,
            'post_tags': post.tags.all(),
            'comment_form': CommentForm(),
            'comments': post.comments.all().order_by('-id'),
            'is_saved_for_later': self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)


    def post(self , request, slug ):
        comment_form = CommentForm(request.POST) #포스트 요청을 통해 전달된 데이터로 댓글 폼을 생성
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post #모델 설정시 포스트 객체로 연관관계 맵핑 했기에 객체를 통째로 넘겨야함
            comment.save()
            return HttpResponseRedirect(reverse('post-detail-page', args=[slug]))


        context = {
            'post': post,
            'post_tags': post.tags.all(),
            'comment_form': comment_form,
            'comments': post.comments.all().order_by('-id'),
            'is_saved_for_later': self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)





    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["post_tags"] = self.object.tags.all()
    #     context["comment_form"] = CommentForm()
    #     return context


# def post_detail(request, slug):
#     #identified_post = next(post for post in all_posts if post['slug'] == slug) # next는 첫번째 요소 반환
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post-detail.html", {
#       "post": identified_post,
#       "post_tags": identified_post.tags.all()
#     })
class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get('stored_posts')

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context['posts'] = posts
            context['has_posts'] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get('stored_posts')

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session['stored_posts'] = stored_posts
        return HttpResponseRedirect("/")