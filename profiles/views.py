from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def userProfile(request):
    user = request.user
    context = {'user': user}
    template = 'profiles/profile/profile.html'
    return render(request, template, context)
