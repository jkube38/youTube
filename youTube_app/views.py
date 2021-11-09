from django.shortcuts import redirect, render, reverse
from django.contrib.auth import login, logout, authenticate
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from pytube import YouTube
from django.contrib.auth.decorators import login_required
from youTube_app.forms import YouTubeLinkInput, YouTubeStream, SignUpForm
from youTube_app.forms import LoginForm, UpdateUserForm, ResetRequest
from youTube_app.forms import ResetPasswordForm
from youTube_app.models import DownloadUser, TemporaryUrl, VidData
from youTube_app.helper_functions import string_generator, thumbs_for_display


# Create your views here.
# Home page for loggin in
def index_view(request):
    context = {}
    form_background = thumbs_for_display(3)

    unique_username = ''
    unique_email = ''
    passwords = ''

    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            check_username = DownloadUser.objects.filter(
                username=data['username']).exists()
            check_email = DownloadUser.objects.filter(
                email=data['email']).exists()
            if check_username and check_email:
                unique_username = f'{data["username"]} is already in use!'
                unique_email = f'{data["email"]} is already in use!'
            elif check_username:
                unique_username = f'{data["username"]} is already in use!'
            elif check_email:
                unique_email = f'{data["email"]} is already in use!'
            else:
                if data['password'] == data['password2']:
                    DownloadUser.objects.create(
                        username=data['username'],
                        email=data['email'],
                        password=data['password'],
                        download_path=data['path']
                    )
                    print('STUCK IN FORM IS VALID')
                    new_user = DownloadUser.objects.get(
                        username=data['username'])
                    new_user.set_password(data['password'])
                    new_user.save()
                    return redirect(reverse('login'))
                else:
                    passwords = 'Passwords Do not match'

    print(request)
    form = SignUpForm()
    context.update({
        'form': form,
        'unique_username': unique_username,
        'unique_email': unique_email,
        'passwords': passwords,
        'form_background': form_background
    })
    return render(request, 'index.html', context)


# Login Page
def login_view(request):
    context = {}
    login_error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data['username'],
                password=data['password']
            )
            print(user)
            if user:
                login(request, user)
                user = DownloadUser.objects.get(username=user)
                return redirect('profile', user)
            else:
                login_error = 'username or password is incorrect'

    form = LoginForm()
    context.update({
        'form': form,
        'login_error': login_error
    })
    return render(request, 'login.html', context)


# Users Profile
@login_required(login_url='/login/')
def profile_view(request, username):
    context = {}
    user = request.user
    user_downloads = user.downloads.all()

    form = YouTubeLinkInput()
    if request.method == 'POST':
        form = YouTubeLinkInput(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            yt_link = data['yt_link']
            request.session['yt_link'] = (yt_link)
            return redirect(reverse('results'))

    form = YouTubeLinkInput()
    context.update({
        'form': form,
        'user_downloads': user_downloads
        })
    return render(request, 'profile.html', context)


# Logging Out
def logout_view(request):
    logout(request)
    return redirect(reverse('home'))


# Display results of submitted link and allows user to choose
# stream to download
@login_required(login_url='/login/')
def results_view(request):
    context = {}
    path = request.user.download_path
    username = request.user.username

    yt_link = request.session.get('yt_link')
    yt = YouTube(yt_link)
    print(yt.keywords)
    form = YouTubeStream()
    if request.method == 'POST':
        form = YouTubeStream(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            stream_num = data['yt_stream']
            stream = yt.streams.get_by_itag(stream_num)
            stream.download(path)

            check_downloads = VidData.objects.filter(url=yt_link)
            if not check_downloads:
                download = VidData.objects.create(
                    thumb=yt.thumbnail_url,
                    title=yt.title,
                    url=yt_link
                )
                user = request.user
                user.downloads.add(download)
            else:
                download = VidData.objects.get(url=yt_link)
                user = request.user
                user.downloads.add(download)

            return redirect('profile', username)

    context.update({
        'yt': yt,
        'form': form,
        'path': path
    })
    return render(request, 'results.html', context)


# Updates users profile
@login_required(login_url='/login/')
def update_profile_view(request, username):
    context = {}
    if request.method == 'POST':
        form = UpdateUserForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            print('DOWNLOAD', request.FILES)
            return redirect('profile', username)
    else:
        form = UpdateUserForm(initial={
            'username': request.user.username,
            'email': request.user.email,
            'download_path': request.user.download_path,
            'user_pic': request.user.user_pic
        })

    context.update({
        'form': form
    })

    return render(request, 'update_profile.html', context)


# Forgot Password Reset Form
def reset_request_view(request):
    context = {}
    address = ''
    request_user = None
    form = ResetRequest()
    if request.method == 'POST':
        form = ResetRequest(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            address = data['email']
            user = DownloadUser.objects.get(email=address)
            request_user = user.username
            random_string = string_generator()

            TemporaryUrl.objects.create(
                snippet=random_string,
                user=request_user
            )

            random_snippet = TemporaryUrl.objects.get(snippet=random_string)

            # Email Data
            subject = 'YouTube/Downloader Password Reset'
            from_email = None
            to = address
            text_content = 'Follow the link to reset your password'
            html_content = render_to_string('email.html', {
                'request_user': request_user,
                'random_snippet': random_snippet.snippet
                })

            # Email Config
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

    context.update({
        'form': form,
        'address': address,
        'request_user': request_user
    })
    return render(request, 'reset_request.html', context)


def password_reset_view(request, username, snippet):
    temporary = TemporaryUrl.objects.get(snippet=snippet)
    if temporary:
        context = {}
        temporary.delete()
        form = ResetPasswordForm()
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_password = data['password']
                retype = data['password2']

                if new_password == retype:
                    user = DownloadUser.objects.get(username=username)
                    user.set_password(new_password)
                    user.save()
                    return redirect(reverse('login'))

        context.update({
            'form': form
        })

        return render(request, 'password_reset.html', context)
