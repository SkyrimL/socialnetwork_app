from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404


from django.utils import timezone

from socialnetwork.forms import LoginForm, RegisterForm, PostForm, ProfileForm
from socialnetwork.models import Post, Profile, Comment

import json


def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)


def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))



@login_required(login_url='login')
def stream(request):
    if request.method == "GET":
        return render(request, 'socialnetwork/globalStream.html', {'posts':Post.objects.all().order_by('-post_time')})

    new_post=Post(post_text=request.POST['post_input_text'],post_by=request.user,post_time=timezone.now())
    new_post.save()
    return render(request, 'socialnetwork/globalStream.html', {'posts':Post.objects.all().order_by('-post_time')})




def get_stream(request, post=None):

    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    stream = []

    if not post:
        post=Post.objects.all()
    else:
        post=[post]
    
    for i in post:
        json_item = {
            'id': i.id,
            'user_id':i.post_by.id,
            'first_name': i.post_by.first_name,
            'last_name': i.post_by.last_name,
            'post_text': i.post_text,
            'post_time': timezone.localtime(i.post_time).strftime("%m/%d/%Y %#I:%M %p"),
            'comments':[]
        }
        


        for j in Comment.objects.filter(comment_is_under_post__exact = i):
            comment_item={
                'id': j.id,
                'first_name': j.comment_by.first_name,
                'last_name': j.comment_by.last_name,
                'comment_text': j.comment_text,
                'comment_time': timezone.localtime(j.comment_time).strftime("%m/%d/%Y %#I:%M %p")
            }
            json_item['comments'].append(comment_item)
        stream.append(json_item)

    result = json.dumps(stream)
    response = HttpResponse(result, content_type='application/json')
    return response



def get_follower(request):

    stream = []
    profile = Profile.objects.get(user=request.user)
    follow = profile.following.all()
    
    for i in Post.objects.filter(post_by__in=follow):
        json_item = {
            'id': i.id,
            'user_id':i.post_by.id,
            'first_name': i.post_by.first_name,
            'last_name': i.post_by.last_name,
            'post_text': i.post_text,
            'post_time': timezone.localtime(i.post_time).strftime("%m/%d/%Y %#I:%M %p"),
            'comments':[]
        }
        


        for j in Comment.objects.filter(comment_is_under_post__exact = i):
            if j.comment_by.id in follow.values_list("id",flat=True) or j.comment_by.id==request.user.id:
                comment_item={
                    'id': j.id,
                    'first_name': j.comment_by.first_name,
                    'last_name': j.comment_by.last_name,
                    'comment_text': j.comment_text,
                    'comment_time': timezone.localtime(j.comment_time).strftime("%m/%d/%Y %#I:%M %p")
                }
            json_item['comments'].append(comment_item)
        stream.append(json_item)

    result = json.dumps(stream)
    response = HttpResponse(result, content_type='application/json')
    return response


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    new_user.save()

    #这里如果用原有的账户登录 没有新注册过 就没有profile，要测试需要
    profile=Profile(bio = '3333',user= new_user,picture = None,content_type='image')
    profile.save()


    login(request, new_user)
    return redirect(reverse('home'))


@login_required(login_url='login')
def followerStream(request):
    if request.method == "GET":
        return render(request, 'socialnetwork/followerStream.html', {'posts':Post.objects.all().order_by('-post_time')})


@login_required(login_url='login')
def myProfile(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    #这快一定要在终端里migrate一下，那个table才会创建，好几次了，他说找不到talble估计就是没migrate!!!
    if request.method == "GET":
        context={'profile': request.user.profile,
        'form': ProfileForm(initial={'bio': request.user.profile.bio})}
        return render(request, 'socialnetwork/myProfile.html', context)
    #这个form应该就是传到html里面的那个
    form = ProfileForm(request.POST, request.FILES, instance=profile)

    if not form.is_valid():
        context['form'] = form
        context['profile'] = profile
        return render(request, 'socialnetwork/myProfile.html', context)

    pic = form.cleaned_data['picture']
    print('Uploaded picture: {} (type={})'.format(pic, type(pic)))
    profile.bio = form.cleaned_data['bio']
    profile.picture = form.cleaned_data['picture']
    profile.content_type = form.cleaned_data['picture'].content_type
    profile.save()

    context['form'] = form
    context['profile'] = profile
    return render(request, 'socialnetwork/myProfile.html', context)


@login_required(login_url='login')
def otherProfile(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, 'socialnetwork/otherProfile.html', {'profile':user.profile})




@login_required(login_url='login')
def get_photo(request, id):
    item = get_object_or_404(Profile, id=id)
    print('Picture #{} fetched from db: {} (type={})'.format(id, item.picture, type(item.picture)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not item.picture:
        raise Http404

    return HttpResponse(item.picture, content_type=item.content_type)


@login_required(login_url='login')
def unfollow(request, id):
    user_to_unfollow = get_object_or_404(User, id=id)
    request.user.profile.following.remove(user_to_unfollow)
    request.user.profile.save()
    return render(request, 'socialnetwork/otherProfile.html', {'profile':user_to_unfollow.profile})

@login_required(login_url='login')
def follow(request, id):
    user_to_follow = get_object_or_404(User, id=id)
    request.user.profile.following.add(user_to_follow)
    request.user.profile.save()
    return render(request, 'socialnetwork/otherProfile.html', {'profile':user_to_follow.profile})


def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)


def add_comment(request):
    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)


    if not 'post_id' in request.POST or not request.POST['post_id']:
        return _my_json_error_response("You must be logged in to do this operation", status=400)


    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        return _my_json_error_response("You must enter an item to add.", status=400)

    if not request.POST['post_id'].isnumeric():
        return _my_json_error_response("You must enter an item to add.", status=400)


    try:
        post=Post.objects.get(id=request.POST['post_id'])
        new_item = Comment(comment_by=request.user,comment_is_under_post=post,comment_text=request.POST['comment_text'],comment_time=timezone.now())
        new_item.save()
    except: 
        return HttpResponse("error", content_type='application/json',status=400)

    return get_stream(request, post)