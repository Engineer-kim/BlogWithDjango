from django.shortcuts import render , get_object_or_404
from  .models import Post

all_posts = [

]
# Create your views here.


def starting_page(request):
    latest_posts = Post.objects.all().order_by("-date")[:3]
    #sorted_posts = sorted(all_posts, key=get_date) # 단순히 sort 사용하면 분류된 새로운 배열이 생성되므로 sorted 사용해야함
    #latest_posts = sorted_posts[-3:] #끝에서 3번째 사용 , :-3은 끝에서 3개 제외한 나머지 반환
    return render(request, "blog/index.html", {
      "posts": latest_posts
    })


def posts(request):
    return render(request, "blog/all-posts.html", {
      "all_posts": Post.objects.all().order_by("-date")
    })


def post_detail(request, slug):
    #identified_post = next(post for post in all_posts if post['slug'] == slug) # next는 첫번째 요소 반환
    identified_post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-detail.html", {
      "post": identified_post,
      "post_tags": identified_post.tags.all()
    })