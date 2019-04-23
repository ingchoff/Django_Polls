from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect

# Create your views here.
from .forms import PollForm, CommentForm, QuestionForm, MyLoginForm, ChangePasswordForm
from .models import Poll, Question, Answer, Comment


def index(request):
    # context = {
    #     'page_title': 'My Polls',
    #     'polls_list': poll_list
    # }
    # poll_list = Poll.objects.annotate(question_count=Count('question'))
    # print(request.user.password)
    poll_list = Poll.objects.filter(del_flag=False).annotate(question_count=Count('question'))

    # for poll in poll_list:
    #     question_count = Question.objects.filter(poll_id=poll.id).count()
    #     poll.question_count = question_count

    context = {
        'page_title': 'My Polls',
        'poll_list': poll_list
    }

    return render(request, template_name='polls/index.html', context=context)
    # return HttpResponse("Hello world, welcome to your first view.")


@login_required
@permission_required('polls.view_poll')
def detail(request, poll_id):

    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':
        for question in poll.question_set.all():
            name = 'choice' + str(question.id)
            choice_id = request.POST.get(name)

            if choice_id:
                try:
                    ans = Answer.objects.get(question_id=question.id)
                    ans.choice_id = choice_id
                    ans.save()
                except Answer.DoesNotExist:
                    Answer.objects.create(
                        choice_id=choice_id,
                        question_id=question.id
                    )
    # context = {
    #     'page_title': 'Poll: ',
    #
    #     'qus_list': poll_list[poll_id-1]
    # }
    return render(request, 'polls/detail.html', { 'poll':poll })


@login_required
@permission_required('polls.add_poll')
def create(request):
    if request.method == 'POST':
        form = PollForm(request.POST)

        if form.is_valid():
            poll = Poll.objects.create(
                title=form.cleaned_data.get('title'),
                start_date=form.cleaned_data.get('start_date'),
                end_date=form.cleaned_data.get('end_date')
            )

            for i in range(1, form.cleaned_data.get('no_questions') + 1):
                Question.objects.create(
                    text='QQQ' + str(i),
                    type='01',
                    poll=poll
                )

    else:
        form = PollForm()

    context = {'form': form}
    return render(request, 'polls/create.html', context=context)


def comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = Comment.objects.create(
                title=form.cleaned_data.get('title'),
                body=form.cleaned_data.get('body'),
                email=form.cleaned_data.get('email'),
                tel=form.cleaned_data.get('tel')
            )

    else:
        form = CommentForm()

    context = {'form': form}
    return render(request, 'polls/create_comment.html', context=context)


def question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

    else:
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'polls/create_answer.html', context=context)


def my_login(request):
    context = {}
    if request.method == 'POST':
        form = MyLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('user')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next_url = request.POST.get('next_url')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('index')

    else:
        form = MyLoginForm()
        next_url = request.GET.get('next')
        context['form'] = form
        if next_url:
            context['next_url'] = next_url

    context['form'] = form
    return render(request, 'polls/login.html', context=context)


def my_logout(request):
    logout(request)
    return redirect('my_login')


def my_change_pass(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old = form.cleaned_data.get('old_password')
            new = form.cleaned_data.get('new_password')
            user = request.user
            if user.check_password(old):
                user.set_password(new)
                user.save()
                return redirect('my_login')
    else:
        form = ChangePasswordForm()

    context = {'form': form}
    return render(request, 'polls/change_pass.html', context=context)
