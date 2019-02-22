from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.views import generic
from django.urls import reverse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import Permission, User
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.utils.text import slugify
from random import randint
from faker import Faker
import random

from .models import *
# Create your views here.


def generate_fake_authors(request):
    fake = Faker()
    for x in range(10):
        name = fake.name()
        temp = Author(name=name, contact=fake.phone_number(), date_joined=timezone.now(), slug=slugify(name))
        temp.save()
    return HttpResponse("Done...")


def generate_fake_users(request):
    fake = Faker()
    for x in range(10):
        name = fake.name()
        temp = Author(name=name, contact=fake.phone_number(), date_joined=timezone.now(), slug=slugify(name))
        temp.save()
    return HttpResponse("Done...")


def generate_fake_posts(request):
    fake = Faker()
    existing_authors_pk = Author.objects.values_list('id', flat=True)
    existing_categories_pk = Category.objects.values_list('id', flat=True)
    existing_status_pk = Status.objects.values_list('id', flat=True)
    for x in range(20):
        post_title = fake.sentence(nb_words=randint(4, 8))
        rand_author_id = random.choice(existing_authors_pk)
        rand_category_id = random.choice(existing_categories_pk)
        rand_status_id = random.choice(existing_status_pk)
        # return HttpResponse(rand_author_id)
        temp = Post(post_title=post_title, post_body=fake.paragraphs(nb=randint(3, 10)),
                    keywords=fake.words(nb=3), slug=slugify(post_title),
                    author_id=rand_author_id,
                    category_id=rand_category_id,
                    status_id=4,
                    date_created=timezone.now(),
                    is_featured=True)
        temp.save()
    return HttpResponse("Done...")


def generate_fake_comments(request):
    fake = Faker()
    existing_posts_pk = Post.objects.filter(status__name="Published").values_list('id', flat=True)
    for x in range(150):
        post_id = random.choice(existing_posts_pk)
        temp = Comment(name=fake.name(), comment=fake.paragraphs(nb=1),
                       post_id=post_id, date=fake.date(pattern="%Y-%m-%d", end_datetime=None))
        temp.save()
    return HttpResponse("Done...")


def index(request):
    temp = Paginator(Post.objects.filter(status__name="Published").order_by('-date_created'), 8)
    page = request.GET.get('page')
    posts_list = temp.get_page(page)

    featured_posts = Post.objects.filter(status__name="Published", is_featured=True).order_by('-date_created')[:5]
    categories_list = Category.objects.all()
    authors_list = Author.objects.all()
    return render(request, 'blogmanagement/public/posts.html',
                  {'posts': posts_list, 'featured_posts': featured_posts,
                   'authors': authors_list, 'categories': categories_list,
                   })


def posts_by_author(request, author_slug):
    if request.user.is_superuser:
        author = get_object_or_404(Author, slug=author_slug)
        categories_list = Category.objects.all()
        featured_posts = Post.objects.filter(status__name="Published", is_featured=True).order_by('-date_created')[:5]
        temp = Paginator(Post.objects.filter(author__slug=author_slug).order_by('-date_created'), 8)
        page = request.GET.get('page')
        posts_list = temp.get_page(page)

        if posts_list:
            return render(request, 'blogmanagement/public/posts_by_author.html',
                          {'posts': posts_list, 'author_name': author.user.get_full_name(),
                           'categories': categories_list, 'featured_posts': featured_posts})
        else:
            other_posts = Post.objects.all()
            return render(request, 'blogmanagement/public/posts_by_author.html',
                          {'other_posts': other_posts, 'author_name': author.user.get_full_name()})
    else:
        author = Author.get(slug=author_slug)
        categories_list = Category.objects.all()
        featured_posts = Post.objects.filter(status__name="Published", is_featured=True).order_by('-date_created')[:5]

        temp = Paginator(Post.objects.filter(author__slug=author_slug).order_by('-date_created'), 8)
        page = request.GET.get('page')
        posts_list = temp.get_page(page)
        if posts_list:
            return render(request, 'blogmanagement/public/posts_by_author.html',
                          {'posts': posts_list, 'author_name': author.user.get_full_name(),
                           'categories': categories_list, 'featured_posts': featured_posts})
        else:
            other_posts = Post.objects.all()
            return render(request, 'blogmanagement/public/posts_by_author.html',
                          {'other_posts': other_posts, 'author_name': author.user.get_full_name()})


def posts_by_category(request, category_slug):
    if request.user.is_superuser:
        category_name = get_object_or_404(Category.objects.values('name'), slug=category_slug)
        categories_list = Category.objects.all()
        featured_posts = Post.objects.filter(status__name="Published", is_featured=True).order_by('-date_created')[:5]
        temp = Paginator(Post.objects.filter(category__slug=category_slug).order_by('-date_created'), 8)
        page = request.GET.get('page')
        posts_list = temp.get_page(page)

        if posts_list:
            return render(request, 'blogmanagement/public/posts_by_category.html',
                          {'posts': posts_list, 'category_name': category_name['name'],
                           'categories': categories_list, 'featured_posts': featured_posts})
        else:
            other_posts = Post.objects.all()
            return render(request, 'blogmanagement/public/posts_by_category.html',
                          {'other_posts': other_posts, 'category_name': category_name['name']})
    else:
        category_name = Category.objects.values('name').get(slug=category_slug)
        categories_list = Category.objects.all()
        featured_posts = Post.objects.filter(status__name="Published", is_featured=True).order_by('-date_created')[:5]

        temp = Paginator(Post.objects.filter(category__slug=category_slug).order_by('-date_created'), 8)
        page = request.GET.get('page')
        posts_list = temp.get_page(page)
        if posts_list:
            return render(request, 'blogmanagement/public/posts_by_category.html',
                          {'posts': posts_list, 'category_name': category_name['name'], 'categories': categories_list, 'featured_posts': featured_posts})
        else:
            other_posts = Post.objects.all()
            return render(request, 'blogmanagement/public/posts_by_category.html',
                          {'other_posts': other_posts, 'category_name': category_name['name']})


def publish_post(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.get(pk=post_id)
        post.status_id = 4
        post.save()
        return HttpResponseRedirect(reverse('blogmanagement:posts',))
    else:
        return HttpResponseRedirect(reverse('blogmanagement:login',))


def manage_home(request):
    if request.user.is_authenticated:
        author_count = Author.objects.count()
        published_posts_count = Post.objects.filter(status__name='Published').count()
        pending_posts_count = Post.objects.exclude(status__name="Published").count()
        today = datetime.today()
        seven_days_ago = today - timedelta(days=7)
        comments_count = Comment.objects.filter(date__gte=seven_days_ago).count()

        return render(request, 'blogmanagement/admin/dashboard_home.html',
                      {'author_count': author_count,
                       'published_posts_count': published_posts_count,
                       'pending_posts_count': pending_posts_count,
                       'comments_count': comments_count
                       }
                      )
    else:
        return HttpResponseRedirect(reverse('blogmanagement:login',))


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:manage_home'))
    else:
        if request.method == "GET":
            return render(request, 'blogmanagement/public/login.html',)
        else:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('blogmanagement:manage_home'))
            else:
                return render(request, 'blogmanagement/public/login.html', {'error': "Invalid username or password"})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('blogmanagement:index'))
    else:
        return HttpResponseRedirect(reverse('blogmanagement:index'))


def categories(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.user.has_perm('blogmanagement.view_category'):
        categories_list = Category.objects.all()
        context = {'categories': categories_list}
        return render(request, 'blogmanagement/categories/categories.html', context)
    else:
        raise Http404


def new_category_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.user.has_perm('blogmanagement.new_category'):
        if request.method == "GET":
            return render(request, 'blogmanagement/categories/new_category.html')
        else:
            if request.POST['name'] == "":
                return render(request, 'blogmanagement/categories/new_category.html', {'error': "Name can't be empty."})
            else:
                category = Category(name=request.POST['name'])
                category.save()
                return HttpResponseRedirect(reverse('blogmanagement:categories', ))
    else:
        raise Http404


def delete_category(request, category_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.user.has_perm('blogmanagement.delete_category'):
        category = get_object_or_404(Category, pk=category_id)
        category.delete()
        return render(request, 'blogmanagement/categories/categories.html', {'categories': Category.objects.all(),
                                                                                'success': "Category %s successfully deleted" % category.name
                                                                             })


def category_delete_confirmation_view(request, category_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.user.has_perm('blogmanagement.delete_category'):
        if request.method == "GET":
            category = get_object_or_404(Category, pk=category_id)
            return render(request, 'blogmanagement/categories/delete_confirmation.html', {'category': category})
        else:
            category = get_object_or_404(Category, pk=category_id)
            category.delete()
            return HttpResponseRedirect(reverse('blogmanagement:categories',))
    else:
        raise Http404


def edit_category(request, category_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.user.has_perm('blogmanagement.change_category'):
        if request.method == "GET":
            category = get_object_or_404(Category, pk=category_id)
            return render(request, 'blogmanagement/categories/edit_category.html', {'category': category})
        else:
            if request.POST['name'] == '':
                return render(request, 'blogmanagement/categories/edit_category.html', {'category': Category.objects.get(pk=category_id),
                                                                                     'error': "Name can't be empty."})
            else:
                category = Category.objects.get(pk=request.POST['category_id'])
                category.name = request.POST['name']
                category.save()
                return HttpResponseRedirect(reverse('blogmanagement:categories', ))
    else:
        raise Http404


def authors(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))

    if request.user.has_perm('blogmanagement.view_author'):
        temp = Paginator(Author.objects.order_by('-date_joined'), 8)
        page = request.GET.get('page')
        authors_list = temp.get_page(page)
        return render(request, 'blogmanagement/authors/authors.html', {'authors': authors_list})
    else:
        raise Http404


def new_author_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.user.has_perm('blogmanagement.new_author'):
        if request.method == "GET":
            return render(request, 'blogmanagement/authors/new_author.html')
        else:
            user = User(first_name=request.POST["first_name"], last_name=request.POST["last_name"],
                        username=request.POST["username"],
                        email=request.POST["email"])
            user.set_password(request.POST["password"])
            user.save()
            user.groups.add(1)
            author = Author(user=user, contact=request.POST['contact'], date_joined=user.date_joined, slug=slugify(user.get_full_name()))
            author.save()
            return HttpResponseRedirect(reverse('blogmanagement:authors', ))

    else:
        raise Http404


def author_delete_confirmation_view(request, author_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.user.has_perm('blogmanagement.delete_author'):
        if request.method == "GET":
            author = get_object_or_404(Author, pk=author_id)
            return render(request, 'blogmanagement/authors/delete_confirmation.html', {'author': author})
        else:
            author = get_object_or_404(Author, pk=author_id)
            author.delete()
            return HttpResponseRedirect(reverse('blogmanagement:authors', ))

    else:
        raise Http404


def edit_author_view(request, author_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.user.has_perm('blogmanagement.change_author'):
        if request.method == "GET":
            author = get_object_or_404(Author, pk=author_id)
            return render(request, 'blogmanagement/authors/edit_author.html', {'author': author})
        else:
            if request.POST['name'] == '':
                return render(request, 'blogmanagement/authors/edit_author.html', {'category': Author.objects.get(pk=author_id),
                                                                                     'error': "Name can't be empty."})
            else:
                author = Author.objects.get(pk=request.POST['author_id'])
                author.name = request.POST['name']
                author.save()
                return HttpResponseRedirect(reverse('blogmanagement:authors', ))
    else:
        raise Http404


def status(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.user.has_perm('blogmanagement.view_status'):
        status_list = Status.objects.all()
        return render(request, 'blogmanagement/status/status.html', {'status_list': status_list})

    else:
        raise Http404


def new_status_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.user.has_perm('blogmanagement.new_status'):
        if request.method == "GET":
            return render(request, 'blogmanagement/status/new_status.html')
        else:
            if request.POST['name'] == "":
                return render(request, 'blogmanagement/status/new_status.html', {'error': "Name can't be empty."})
            else:
                status = Status(name=request.POST['name'])
                status.save()
                return HttpResponseRedirect(reverse('blogmanagement:status', ))

    else:
        raise Http404


def status_delete_confirmation_view(request, status_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))

    if request.user.has_perm('blogmanagement.delete_status'):
        if request.method == "GET":
            status_info = get_object_or_404(Status, pk=status_id)
            return render(request, 'blogmanagement/status/delete_confirmation.html', {'status': status_info})
        else:
            status_info = get_object_or_404(Status, pk=status_id)
            status_info.delete()
            return HttpResponseRedirect(reverse('blogmanagement:status', ))

    else:
        raise Http404


def edit_status_view(request, status_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.user.has_perm('blogmanagement.delete_status'):
        if request.method == "GET":
            status_info = get_object_or_404(Status, pk=status_id)
            return render(request, 'blogmanagement/status/edit_status.html', {'status': status_info})
        else:
            if request.POST['name'] == '':
                return render(request, 'blogmanagement/status/edit_status.html', {'status': Status.objects.get(pk=status_id),
                                                                                     'error': "Name can't be empty."})
            else:
                status_info = Status.objects.get(pk=request.POST['status_id'])
                status_info.name = request.POST['name']
                status_info.save()
                return HttpResponseRedirect(reverse('blogmanagement:status', ))

    else:
        raise Http404


def posts_by_status(request, status_slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.user.has_perm('blogmanagement.delete_status'):
        status_name = Status.objects.values('name').get(slug=status_slug)
        posts_list = Post.objects.filter(status__slug=status_slug)
        return render(request, 'blogmanagement/status/posts_by_status.html',
                      {'posts': posts_list, 'status_name': status_name['name']})
    else:
        raise Http404


def posts(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    temp = Paginator(Post.objects.order_by('-date_created'), 8)
    page = request.GET.get('page')
    posts_list = temp.get_page(page)

    return render(request, 'blogmanagement/posts/posts.html', {'posts': posts_list})


def post_detail_view(request, post_slug):
    featured_posts = Post.objects.filter(status__name="Published", is_featured=True).order_by('-date_created')[:5]
    categories_list = Category.objects.all()
    post_info = get_object_or_404(Post, slug=post_slug)
    comments = post_info.comment_set.order_by('-date')[:5]
    comments_count = post_info.comment_set.count()
    return render(request, 'blogmanagement/posts/post_detail.html', {'post': post_info,
                                                                     'featured_posts': featured_posts,
                                                                     'categories': categories_list,
                                                                     'comments': comments,
                                                                     'comments_count': comments_count
                                                                     })


def save_comment(request):
    comment = Comment(name=request.POST['name'], comment=request.POST['comment'],
                      post_id=request.POST['post_id'], date=timezone.now())
    comment.save()
    return HttpResponseRedirect(request.POST['path'])


def new_post_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.method == "GET":
        authors_list = Author.objects.all()
        categories_list = Category.objects.all()
        status_list = Status.objects.all()
        return render(request, 'blogmanagement/posts/new_post.html', {'authors': authors_list,
                                                                      'categories': categories_list,
                                                                      'status': status_list})
    else:
        if request.POST['title'] == "":
            return render(request, 'blogmanagement/posts/new_post.html', {'error': "Title can't be empty."})
        else:
            post = Post(post_title=request.POST['title'], post_body=request.POST['body'],
                        keywords=request.POST['keywords'],
                        author_id=int(request.POST['author']), category_id=int(request.POST['category']),
                        status_id=int(request.POST['status']),
                        date_created=timezone.now(), date_published=timezone.now())

            post.save()
            return HttpResponseRedirect(reverse('blogmanagement:posts', ))


def post_delete_confirmation_view(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.method == "GET":
        post_info = get_object_or_404(Post, pk=post_id)
        return render(request, 'blogmanagement/posts/delete_confirmation.html', {'post': post_info})
    else:
        post_info = get_object_or_404(Post, pk=post_id)
        post_info.delete()
        return HttpResponseRedirect(reverse('blogmanagement:posts', ))


def edit_post_view(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogmanagement:login', ))
    if request.method == "GET":
        authors_list = Author.objects.all()
        categories_list = Category.objects.all()
        status_list = Status.objects.all()
        post_info = get_object_or_404(Post, pk=post_id)
        return render(request, 'blogmanagement/posts/edit_post.html', {'post': post_info, 'authors': authors_list,
                                                                        'categories': categories_list,
                                                                        'status': status_list})
    else:
        if request.POST['title'] == "":
            return render(request, 'blogmanagement/posts/edit_post.html', {'error': "Title can't be empty."})
        else:
            post = Post.objects.get(pk=post_id)
            post.post_title = request.POST['title']
            post.post_body = request.POST['body']
            post.keywords = request.POST['keywords']
            post.author_id = request.POST['author']
            post.category_id = request.POST['category']
            post.status_id = request.POST['status']
            post.save()
            return HttpResponseRedirect(reverse('blogmanagement:posts', ))


