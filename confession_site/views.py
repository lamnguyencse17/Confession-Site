from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from .form import LoginForm, ConfessionForm
from .models import Confession, Moderator, LoginRecord
from .form import LoginForm, ContactForm
from .models import Confession, Moderator, LoginRecord, ContactRecord
from django.contrib.auth.hashers import make_password, check_password
from django.template.loader import render_to_string
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from django.views.decorators.cache import cache_page

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@cache_page(CACHE_TTL)
def index(request):
    form = ConfessionForm()
    return render(request, 'index.html', {'form': form})


def result(request):
    if request.method is 'GET':  # prevent direct access
        raise Http404
    else:
        confess = ConfessionForm(request.POST, request.FILES)
        if confess.is_valid():
            if Confession.objects.filter(confession_text=confess.cleaned_data['confess_content']).first():  # Check form re-submission
                return render(request, 'error.html', {
                    'error_message': "Duplicates found",
                })
            else:
                confession = Confession(confession_text=confess.cleaned_data['confess_content'],confession_picture=confess.cleaned_data['picture'], confess_date=timezone.now(), confession_edited_date=timezone.now())
                confession.save()
                pic_exist = True
                if bool(confession.confession_picture) == False:
                    pic_exist = False
                return render(request, 'result.html', {'confession': confession.confession_text, 'id': confession.id, 'picture': confession.confession_picture, 'exist': pic_exist})
        else:
            raise Http404

def recall(request):
    if request.method == 'GET':  # prevent direct access
        raise Http404
    else:
        confess_id = request.POST.get('confess_id')  # Only for initialize purpose
        if Confession.objects.filter(id=confess_id):
            confession = Confession.objects.get(id = confess_id)
            pic_exist = True
            if bool(confession.confession_picture) == False:
                pic_exist = False
            return render(request, 'recall.html', {'confession': confession.confession_text,
                                                   'status': confession.confession_published,
                                                   'id': confession.id,
                                                   'picture': confession.confession_picture, 'exist': pic_exist})
        else:
            return render(request, 'error.html', {
                'error_message': "you inputted invalid ID",
            })



def error(request):
    if request.method == 'GET':  # prevent direct access
        raise Http404
    else:
        return render(request, 'error.html')


def delete(request):
    if request.method == 'GET':  # prevent direct access
        raise Http404
    else:
        confess_id = request.POST.get('id')
        response_data = {}
        if Confession.objects.filter(id=confess_id):
            confession = Confession.objects.get(id = confess_id)
            confession.delete()
            response_data['result'] = 'Delete successfully'
        else:
            response_data['result'] = 'Delete unsuccessfully'
        return JsonResponse(response_data)


def about(request):
    if request.method == 'GET':
        contact = ContactForm()
        return render(request, 'about.html', {'form': contact})
    else:
        response_data = {}
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        print(name)
        print(email)
        print(content)
        Contact = ContactRecord(name = name, email = email, content = content)
        Contact.save()
        response_data['result'] = "Succeeded!"
        return JsonResponse(response_data)


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

@csrf_exempt
@cache_page(CACHE_TTL)
def manage(request):
    try:
        request.session['username']
    except KeyError:
        return render(request, 'error.html', {
            'error_message': "Not logged in yet!",
        })
    confess_list = Confession.objects.filter(confession_published="Unpublished").order_by('-confess_date')
    paginator = Paginator(confess_list, 5)
    #Experimental
    if (request.method == "GET"):
        page_number = request.GET.get("page_number")
        paginator = Paginator(confess_list, 5)
        try:
            confessions = paginator.page(page_number)
        except PageNotAnInteger:
            confessions = paginator.page(1)
        except EmptyPage:
            confessions = paginator.page(paginator.num_pages)
        return render(request, 'manage.html', {'list': confessions, 'user': request.session['username']})
    else:
        page_number = request.POST.get("page_number")
        paginator = Paginator(confess_list, 5)
        if (paginator.page(int(page_number)-1)).has_next() is False:
            return HttpResponse('No More')
        try:
            confessions = paginator.page(page_number)
        except PageNotAnInteger:
            confessions = paginator.page(1)
        except EmptyPage:
            confessions = paginator.page(paginator.num_pages)
        csrf_token_value = get_token(request)
        html = render_to_string('posts.html', {'list': confessions, 'user': request.session['username'], 'csrf_token_value': csrf_token_value})
        return HttpResponse(html)

@csrf_exempt
def edit_post(request):
    if request.method == 'POST':
        confession_id = request.POST.get('id')
        confession_edit = request.POST.get('confession_edit')
        user_session = request.POST.get('user')
        response_data = {}
        try:
            editor = Moderator.objects.get(username=user_session)
            Confession.objects.filter(id=confession_id).update(confession_edited_by=editor)
            edit = Confession.objects.get(id=confession_id)
            edit.confession_text = confession_edit
            edit.confession_edited = 'Yes'
            edit.confession_edited_by = Moderator.objects.get(username=user_session)
            edit.confession_edited_date = timezone.now()
            edit.save()
            response_data['result'] = 'Edit successfully'
            response_data['edit'] = confession_edit
            return JsonResponse(response_data)
        except (edit.DoesNotExist, ValueError):
            return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
