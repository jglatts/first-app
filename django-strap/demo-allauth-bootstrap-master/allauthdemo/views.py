import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .auth.models import Question, Choice
from .auth.forms import NewBlog

@login_required
def member_index(request):
    t = loader.get_template('member/member-index.html')
    c = {}  #{'foo': 'bar'}
    return HttpResponse(t.render(c, request), content_type='text/html')

@login_required
def member_action(request):
    t = loader.get_template('member/member-action.html')
    c = {}  #{'foo': 'bar'}
    return HttpResponse(t.render(c, request), content_type='text/html')


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:15]
    # Only displays ONE entry, have to be able to show ALL entries
    # For ALL blog posts. Not in use, somewhat functionaly though 
    question = get_object_or_404(Question, pk=2)
    template = loader.get_template('visitor/question.html')
    context = {
        'latest_question_list': latest_question_list,
        'question': question
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'visitor/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'visitor/results.html', {'question': question})

    if request.method == "POST":
        if form0.is_valid():
            post = form0.save(commit=False)
            post.pub_date = datetime.datetime.now()
            post.save()
            return render(request, 'visitor/question.html')
    else:
        form = NewBlog()
    return render(request, 'visitor/newblog.html', {'form': form})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'visitor/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(question.id,)))

def new_blog_post(request):
    if request.method == "POST":
        form = NewBlog(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # This handles the 'pub_date'
            # W/out it, the POST does not work
            post.pub_date = datetime.datetime.now()
            post.save()
            return redirect('all_questions')
    else:
        form = NewBlog()
    return render(request, 'visitor/newblog.html', {'form': form})
