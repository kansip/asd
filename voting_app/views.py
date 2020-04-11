import json
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from voting_app.forms import LoginForm, VotingForm, RegisterForm
from voting_app.menu import get_context_menu, REGISTER_PAGE_NAME, LOGIN_PAGE_NAME, VOTES_PAGE_NAME, VOTE_PAGE_NAME, \
    USER_VOTES_PAGE_NAME, VOTES_EDITOR_PAGE_NAME, USER_PAGE_NAME
from voting_app.models import UserVote, Vote, VoteVariant, UserLike


def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return redirect('/votes')


def register_view(request):
    context = {'menu': get_context_menu(request, REGISTER_PAGE_NAME)}

    if request.method == 'POST':
        errors = []

        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            login_data = register_form.cleaned_data['login']
            password_data = register_form.cleaned_data['password']
            password_repeat_data = register_form.cleaned_data['password_repeat']

            if len(login_data) < 5:
                errors.append('Логин должен иметь длину больше 5 символов')

            if User.objects.filter(username=login_data).exists():
                errors.append('Пользователь с таким логином уже существует')

            if len(password_data) < 6:
                errors.append('Пароль должен иметь длину больше 6 символов')

            if password_data != password_repeat_data:
                errors.append('Пароли не совпадают')

            if len(errors) == 0:
                user = User.objects.create_user(username=login_data, password=password_data)
                user.save()

                if user is not None:
                    login(request, user)
                    return redirect('/')

                return redirect('/')
        else:
            errors.append('Заполните все поля')

        context['error'] = errors[0]

    return render(request, 'auth/register.html', context)


def login_view(request):
    context = {'menu': get_context_menu(request, LOGIN_PAGE_NAME)}

    if not request.user.is_authenticated:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)

            if login_form.is_valid():
                login_data = login_form.cleaned_data['login']
                password_data = login_form.cleaned_data['password']

                print(login_data)
                print(password_data)

                user = authenticate(request, username=login_data, password=password_data)

                if user is not None:
                    login(request, user)
                    return redirect('/')

            context['error'] = 'Неверный логин или пароль'

        return render(request, 'auth/login.html', context)
    else:
        return redirect('/')


@login_required
def user_page_view(request, user_id):
    context = {'menu': get_context_menu(request, USER_PAGE_NAME)}

    user = User.objects.get(pk=user_id)

    if request.user.is_authenticated and user:
        context['user'] = user
        return render(request, 'user/user.html', context)

    return redirect('/')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def votes_view(request):
    votes = Vote.objects.all().order_by('-start_at')
    if request.method == "POST":
        if request.POST['if_like'] == "1":
            user_like = UserLike(user=request.user, vote=votes[int(request.POST['vote'])-1], created_at=datetime.today())
            vote = votes[int(request.POST['vote']) - 1]
            vote.liked += 1
            vote.save()
            user_like.save()
        elif request.POST['if_dislike'] == '1':
            user_like = UserLike.objects.get(user=request.user, vote=votes[int(request.POST['vote'])-1])
            vote = votes[int(request.POST['vote']) - 1]
            vote.liked -= 1
            vote.save()
            user_like.delete()
    votes = Vote.objects.all().order_by('-start_at')
    for vote in votes:
        vote.is_voted = UserVote.objects.filter(user=request.user, vote=vote).exists()
        vote.is_liked = UserLike.objects.filter(user=request.user, vote=vote).exists()

    context = {'menu': get_context_menu(request, VOTES_PAGE_NAME), 'items': votes}

    return render(request, 'votes.html', context)


# Страница голосования
@login_required
def vote_view(request, vote_id):
    context = {}

    vote = get_object_or_404(Vote, pk=vote_id)
    is_voted = UserVote.objects.filter(user=request.user, vote=vote).exists()

    if is_voted:
        return redirect('/')

    context['title'] = vote.title

    if request.method == 'POST':
        voting_form = VotingForm(request.POST)

        if voting_form.is_valid():
            variant_id = int(voting_form.cleaned_data['option'])
            vote_variant = VoteVariant.objects.get(pk=variant_id)

            vote = UserVote(user=request.user, vote=vote, vote_variant=vote_variant, created_at=datetime.today())
            vote.save()

            return redirect('/')

    context['menu'] = get_context_menu(request, VOTE_PAGE_NAME)

    variants = VoteVariant.objects.filter(vote=vote)

    context['vote'] = vote
    context['variants'] = variants

    return render(request, 'vote.html', context)


@login_required
def votes_editor_view(request):
    context = {'menu': get_context_menu(request, VOTES_EDITOR_PAGE_NAME),
               'items': Vote.objects.filter(user=request.user).order_by('-start_at')}

    return render(request, 'votes_editor.html', context)


@login_required
def get_vote_view(request, vote_id):
    context = {}

    if request.method == 'POST':
        vote = Vote.objects.get(pk=vote_id, user=request.user)

        if vote:
            context["title"] = vote.title

            vote_variants = VoteVariant.objects.filter(vote=vote)
            variants = []

            for vote_variant in vote_variants:
                variant = {"title": vote_variant.title}
                variants.append(variant)

            context["variants"] = variants

    return HttpResponse(json.dumps(context, cls=DjangoJSONEncoder))


@login_required
def vote_create_view(request):
    context = {}

    if request.method == 'POST':
        errors = []

        vote_title = request.POST.get('vote-title')
        variants_count = int(request.POST.get('variants-count'))

        variants = []

        for i in range(variants_count):
            variants.append(request.POST.get(str(i)))

        if len(vote_title) < 5:
            errors.append('Название голосования должно быть больше 5 символов')

        if len(variants) < 2:
            errors.append('Минимальное количество вариантов — 2')

        for variant in variants:
            if len(variant) < 2:
                errors.append('Название варианта должно быть больше 2 символов')

        if len(errors) == 0:
            vote = Vote(user=request.user, title=vote_title, liked=0, start_at=datetime.now(), end_at=datetime.now())
            vote.save()

            for vote_variant in variants:
                vote_variant = VoteVariant(vote=vote, title=vote_variant)
                vote_variant.save()

            context['success'] = True
        else:
            context['error'] = errors[0]

    return HttpResponse(json.dumps(context))


@login_required
def vote_edit_view(request, vote_id):
    context = {}

    if request.method == 'POST':
        errors = []

        vote = Vote.objects.get(pk=vote_id, user=request.user)

        if not vote:
            errors.append('Данное голосование ещё не создано или было удалено')

        vote_title = request.POST.get('vote-title')
        variants_count = int(request.POST.get('variants-count'))

        variants = []

        for i in range(variants_count):
            variants.append(request.POST.get(str(i)))

        if len(vote_title) < 5:
            errors.append('Название голосования должно быть больше 5 символов')

        if len(variants) < 2:
            errors.append('Минимальное количество вариантов — 2')

        for variant in variants:
            if len(variant) < 2:
                errors.append('Название варианта должно быть больше 2 символов')

        if len(errors) == 0:
            if vote:
                # delete all UserVotes
                UserVote.objects.filter(user=request.user, vote=vote).delete()

                vote_variants = VoteVariant.objects.filter(vote=vote)

                vote.title = vote_title
                vote.save()

                # changes
                for i in range(len(variants)):
                    variant_title = variants[i]

                    if i < len(vote_variants):
                        vote_variant = vote_variants[i]
                        vote_variant.title = variant_title
                        vote_variant.save()
                    else:
                        vote_variant = VoteVariant(vote=vote, title=variant_title)
                        vote_variant.save()

                # remove
                for i in range(len(vote_variants)):
                    vote_variant = vote_variants[i]

                    if i >= len(variants):
                        vote_variant.delete()

                context['success'] = True

        else:
            context['error'] = errors[0]

    return HttpResponse(json.dumps(context, cls=DjangoJSONEncoder))


@login_required
def vote_delete_view(request, vote_id):
    context = {}

    if request.method == 'POST':
        vote = Vote.objects.get(pk=vote_id, user=request.user)

        if vote:
            # delete all UserVotes
            UserVote.objects.filter(user=request.user, vote=vote).delete()

            # delete Vote
            vote.delete()

            context["success"] = True

    return HttpResponse(json.dumps(context))


# Список голосов юзера
@login_required
def user_votes_view(request):
    user_votes = UserVote.objects.filter(user=request.user).order_by('-created_at')

    context = {'menu': get_context_menu(request, USER_VOTES_PAGE_NAME),
               'items': user_votes}

    return render(request, 'user/votes.html', context)
