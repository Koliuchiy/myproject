from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Producer, Article
from cart.forms import CartAddArticleForm
from . import forms


# Create your views here.
def home(request):
    categories = Category.objects.all()
    articles = Article.objects.filter(available=True)
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
                messages.error(request, 'Your message not sent. Try again later')
            else:
                messages.success(request, 'Your message is sent!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'shop/contact.html', {'form': form,
                                                         'title': title})
    else:
        form = forms.ContactForm()
        return render(request, 'shop/contact.html', {'form': form, 'title': title})


def category_list(request, category):
    articles = Article.objects.filter(available=True, category__slug=category)
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
    template = 'shop/article_detail.html'
    articles = Article.objects.filter(available=True)
    categories = Category.objects.all()
    art = get_object_or_404(Article, slug=slug)
    cart_article_form = CartAddArticleForm()
    # List of active comments for this post
    comments = art.comments.filter(active=True)
    art_tags_ids = art.tags.values_list('id', flat=True)
    similar_articles = Article.objects.filter(available=True, tags__in=art_tags_ids)\
                                   .exclude(id=art.id)
    similar_articles = similar_articles.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags','-created')[:4]
    return render(request, template, {'articles': articles,
                                      'categories': categories,
                                      'art': art,
                                      'comments': comments,
                                      'similar_articles': similar_articles,
                                      'cart_article_form': cart_article_form})

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
            messages.success(request, 'Your reviews was added!')
            return HttpResponseRedirect(reverse('shop:article_detail', args=[art.slug]))
        else:
            return render(request, template, {'comment_form': comment_form,
                                              'art': art,})
    else:
        comment_form = forms.CommentForm()
        return render(request, template, {'comment_form': comment_form,
                                          'art': art,})
