from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('visitor/question1.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
