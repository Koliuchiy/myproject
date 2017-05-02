from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Article
from .cart import Cart
from .forms import CartAddArticleForm


@require_POST
def cart_add(request, article_id):
    cart = Cart(request)
    article = get_object_or_404(Article, id=article_id)
    form = CartAddArticleForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(article=article, quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, article_id):
    cart = Cart(request)
    article = get_object_or_404(Article, id=int(article_id))
    cart.remove(article)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddArticleForm(initial={
                                       'quantity': item['quantity'],
                                       'update': True})
    return render(request, 'cart/cart_detail.html', {'cart': cart})
