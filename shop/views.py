from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Category, Producer, Article
from . import forms


# Create your views here.
def home(request):
    categories = Category.objects.all()
    articles = Article.availabl.all()
    template = 'shop/home.html'
    paginator = Paginator(articles, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)
    return render(request, template, {'categories': categories,
                                      'articles': articles,
                                      'page': page})


def about(request):
    template = 'shop/about.html'
    return render(request, template)


def contact_admin(request):
    title = "Contact"
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            comment = form.cleaned_data['comment']
            subject = 'message from my site'
            message = '%s %s' %(comment, name)
            recipients = [settings.EMAIL_HOST_USER]
            try:
                send_mail(subject, message, email, recipients)
            except:
                status_message = 'Your message not sent. Try again later'
                type_message = "alert alert-danger"
            else:
                status_message = 'Your message is sent!'
                type_message = "alert alert-success"
            return HttpResponseRedirect('%s?status_message=%s&amp;type_message=%s'
                                        % (reverse('contact'), status_message, type_message))
        else:
            type_message = "alert alert-danger"
            status_message = 'Please enter valid data!'
            return render(request, 'shop/contact.html', {'form': form,
                                                             'title': title,
                                                             'status_message': status_message,
                                                             'type_message': type_message})
    else:
        form = forms.ContactForm(request.POST)
        form = forms.ContactForm()
        return render(request, 'shop/contact.html', {'form': form, 'title': title})


@login_required
def userProfile(request):
    user = request.user
    context = {'user': user}
    template = 'shop/profile.html'
    return render(request, template, context)


def category_list(request, category):
    articles = Article.availabl.filter(category__slug=category)
    categories = Category.objects.all()
    template = 'shop/category_list.html'
    paginator = Paginator(articles, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)
    return render(request, template, {'articles': articles,
                                      'categories': categories,
                                      'page': page})

'''
class ArticleDetailView(DetailView):
    model = Article
    #slug_url_kwarg = 'SLUG_URL_KWARG'
    #success_url = 'SUCCESS_URL'
    template_name = 'category_detail.html'  '''

def article_detail(request, slug):
    articles = Article.availabl.all()
    categories = Category.objects.all()
    template = 'shop/article_detail.html'
    art = get_object_or_404(Article, slug=slug)
    # List of active comments for this post
    comments = art.comments.filter(active=True)
    return render(request, template, {'articles': articles,
                                      'categories': categories,
                                      'art': art,
                                      'comments': comments})

def comment_article(request, slug):
    template = 'shop/comment_article.html'
    art = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        # A comment was posted
        comment_form = forms.CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current article to the comment
            new_comment.article = art
            # Save the comment to the database
            new_comment.save()
            status_message = 'Your reviews was added!'
            type_message= "alert alert-success"
            return HttpResponseRedirect('%s?status_message=%s&amp;type_message=%s'
                                        % (reverse('comment_article'), status_message, type_message))
    else:
        comment_form = forms.CommentForm()
    return render(request, template, {'comment_form': comment_form,
                                      'art': art,})
