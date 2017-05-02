from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def userProfile(request, user_id):
    user = request.user
    context = {'user': user}
    template = 'profiles/profile.html'
    if user.id == int(user_id):
        return render(request, template, context)
    else:
        messages.warning(request, 'Required page is not associated with your account')
        return redirect('shop:home')
