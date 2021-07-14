from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import NewFile, FileForm
import mimetypes
import os


def Home(request):
    if request.method == 'GET':
        return render(request, 'app/home.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request, username= request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'app/login.html', {'form':AuthenticationForm(),'error': 'username and password did not match'})
        else:
            login(request, user)
            return redirect('feed')
#
# def loginuser(request):
#     if request.method == 'GET':
#         return render(request, 'app/login.html',

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'app/signupuser.html', {'form':UserCreationForm()})
    else:
        try:
            if request.POST['password1']  == request.POST['password2']:
                user= User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('Home')
        except IntegrityError:
            return render(request, 'app/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'User already in the system.'})
        else:
            return render(request, 'app/signupuser.html', {'form': UserCreationForm(), 'error': 'passwords did not match'})

def logoutuser(request):
    logout(request)
    return redirect('Home')

@login_required
def feed(request):
    if request.method == 'GET':
        files =  NewFile.objects.filter(user=request.user)
        return render(request, 'app/feed.html', {'files': files})

@login_required
def add(request):
    if request.method == 'GET':
        return render(request, 'app/add_file.html', {'form': FileForm()})
    else:
        try:
            form = FileForm(request.POST, request.FILES)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('feed')
        except ValueError:
            print(form.errors)
            return render(request, 'app/add_file.html', {'form': FileForm(), 'error': 'bad data passed in'})

@login_required
def edit(request, pk):
    todo = get_object_or_404(NewFile, pk=pk, user=request.user)
    if request.method == 'GET':
        form = FileForm(instance=todo)
        return render(request, 'app/viewfile.html', {'todo': todo, 'form':form})

@login_required
def delete(request, pk):
    todo = get_object_or_404(NewFile, pk=pk, user=request.user)
    if request.method == 'GET':
        todo.delete()
        return redirect('feed')


@login_required
def download_file(request, pk):
    file = NewFile.objects.get(pk=pk)
    fl_path = file.the_file.path
    filename = file.the_file.name
    print(file.name)

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

