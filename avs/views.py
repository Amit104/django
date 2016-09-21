from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import UserForm
from .models import UserProfile, CategoriesQ
# Create your views here.

class Counter:
    counter = 1

    def increment(self):
        self.counter += 1
    def set_to_zero(self):
        self.counter = 1
    def get_count(self):
        return self.counter

def home(request):
    if not request.user.is_authenticated():
        return render(request, 'avs/login.html')
    else:
        cs = Counter()
        dic = []
        ccx=0
        s = []
        for i in CategoriesQ.objects.all():
            s.append(i)
            ccx = ccx + 1
            if ccx % 3 == 0:
                dic.append(s)
                s = []
        if not ccx % 3 == 0:
            dic.append(s)
        return render(request, 'avs/home.html', {"category": CategoriesQ.objects.all(),"dic":dic , "x":1 , "c" : cs})



def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'avs/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('avs:home')
            else:
                return render(request, 'avs/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'avs/login.html', {'error_message': 'Invalid login'})
    return render(request, 'avs/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        userprofile = UserProfile(user=user,score=0)
        userprofile.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #albums = Album.objects.filter(user=request.user)
                return redirect('avs:home')
    context = {
        "form": form,
    }
    return render(request, 'avs/register.html', context)
