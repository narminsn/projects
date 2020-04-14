from django.contrib import messages
from django.shortcuts import render, redirect
from user_app.models import MyUser, TokenModel
from user_app.forms import MyUserCreationForm, LoginForm, Security, MyUserChangeForm
from django.contrib.auth import login as auth_login, logout, authenticate


# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    """
    This function is
    performed to
    register users.

    """
    context = {'form': MyUserCreationForm()}
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')

    return render(request, 'register.html', context)


def verify_view(request, token, id):
    verify = TokenModel.objects.filter(
        token=token,
        expired=False,
        user_id=id
    ).last()
    if verify:
        verify.user.is_active = True
        verify.user.save()
        verify.expired = True
        verify.save()
        return redirect('login')
    else:
        return redirect('index')


def login_user(request):
    context = {}
    form = LoginForm
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user:

                auth_login(request, user)
                return redirect('/')
            else:
                messages.error(
                    request, "Username or Password inValid"
                )

    context['form'] = form
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect("/")


def change_password(request):
    context = {}

    context["form"] = Security()

    if request.method == "POST":
        form = Security(request.POST)
        if form.is_valid():
            check = request.user.check_password(form.cleaned_data.get("CurrentPassword"))
            if check:
                request.user.set_password(form.cleaned_data.get("Newpassword"))
                request.user.save()
                return redirect('index')

    return render(request, 'change_password.html', context)


def settings_user(request, id):
    context = {}
    user = MyUser.objects.filter(id=id).last()
    context['form'] = MyUserChangeForm(instance=user)
    if request.method == 'POST':
        form = MyUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'usr_settings.html', context)
