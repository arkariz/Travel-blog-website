from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.db.models import Count

def get_category_count():
  queryset = Post \
    .objects \
    .values('categories__title') \
    .annotate(Count('categories__title'))
  return queryset

def index(request):
  category_count = get_category_count()
  post_list = Post.objects.order_by('-timestamp')
  popular_post = Post.objects.order_by('-comment_count')[:3]
  paginator = Paginator(post_list, 4)
  page_request_var = 'page'
  page = request.GET.get(page_request_var)

  try:
    paginated_queryset = paginator.page(page)
  except PageNotAnInteger:
    paginated_queryset = paginator.page(1)
  except EmptyPage:
    paginated_queryset = paginator.page(paginator.num_pages)

  context = {
    'post_list':paginated_queryset,
    'popular_post':popular_post,
    'category_count':category_count,
    'page_request_var':page_request_var
  }
  return render(request, 'index.html', context)

def post(request, id):
  return render(request, 'post-detail', {})