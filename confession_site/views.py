from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.utils import timezone
from .form import LoginForm
from .models import Confession, Moderator, LoginRecord
from django.contrib.auth.hashers import make_password, check_password


def index(request):
    return render(request, 'index.html')


def result(request):
    if request.method is 'GET':  # prevent direct access
        raise Http404
    else:
        confess = request.POST.get('confess_content')
        if confess is '':  # Validate POST data
            return render(request, 'error.html', {
                'error_message': "you didn't send any content",
            })
        else:
            if Confession.objects.filter(confession_text=confess).first():  # Check form re-submission
                return render(request, 'error.html', {
                    'error_message': "Duplicates found",
                })
            else:
                confession = Confession(confession_text=confess, confess_date=timezone.now())
                confession.save()
                return render(request, 'result.html', {'confession': confession.confession_text, 'id': confession.id})


def recall(request):
    if request.method == 'GET':  # prevent direct access
        raise Http404
    else:
        confess_id = request.POST.get('confess_id')  # Only for initialize purpose
        confession = Confession.objects.get(id=1)
        try:  # Validate POST data
            confession = Confession.objects.get(id=confess_id)
        except (confession.DoesNotExist, ValueError):
            return render(request, 'error.html', {
                'error_message': "you inputted invalid ID",
            })
        return render(request, 'recall.html', {'confession': confession.confession_text,
                                               'status': confession.confession_published,
                                               'id': confession.id})


def error(request):
    if request.method == 'GET':  # prevent direct access
        raise Http404
    else:
        return render(request, 'error.html')


def delete(request):
    if request.method == 'GET':  # prevent direct access
        raise Http404
    else:
        confess_id = request.POST.get('confess_id')
        confession = Confession.objects.get(id=2)
        try:
            confession = Confession.objects.get(id=confess_id)
        except (confession.DoesNotExist, ValueError):
            return render(request, 'error.html', {
                'error_message': "you inputted invalid ID",
            })
        confession.delete()
        return render(request, 'delete.html')


def about(request):
    return render(request, 'about.html')


def recall_index(request):
    return render(request, 'recall-index.html')


def login(request):
    if request.method == 'GET':
        try:
            request.session['username']
            return HttpResponseRedirect('/manage/')
        except KeyError:
            pass
    form = LoginForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        if Moderator.objects.filter(username=form.cleaned_data['username']):
            validate = Moderator.objects.get(username=form.cleaned_data['username'])
            if check_password(form.cleaned_data['password'], validate.hash):
                request.session['username'] = form.cleaned_data['username']
                request.session.set_expiry(300)
                return HttpResponseRedirect('/manage/')
            else:
                return render(request, 'error.html', {
                    'error_message': "Wrong credential",
                })
        else:
            return render(request, 'error.html', {
                'error_message': "Wrong credential",
            })
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    form = LoginForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        mod = Moderator(username=form.cleaned_data['username'], hash=make_password(form.cleaned_data['password']))
        mod.save()
        return HttpResponseRedirect('/login/')
    else:
        form = LoginForm()
    return render(request, 'register.html', {'form': form})


def logout(request):
    try:
        del request.session['username']
    except KeyError:
        return render(request, 'error.html', {
            'error_message': "Not logged in",
        })
    return render(request, 'logout.html')


def manage(request):
    try:
        request.session['username']
    except KeyError:
        return render(request, 'error.html', {
            'error_message': "Not logged in yet!",
        })
    confess_list = Confession.objects.filter(confession_published="Unpublished").order_by('-confess_date')
    return render(request, 'manage.html', {'user': request.session['username'], 'list': confess_list})
