"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
  1. Add an import:  from my_app import views
  2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
  1. Add an import:  from other_app.views import Home
  2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
  1. Import the include() function: from django.conf.urls import url, include
  2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from .auth.views import account_profile
from .views import member_index, member_action, index, detail, vote, results
from .views import new_blog_post
from . import views

urlpatterns = [
    # Landing page area
    url(r'^$', TemplateView.as_view(template_name='visitor/landing-index.html'), name='landing_index'),
    url(r'^about$', TemplateView.as_view(template_name='visitor/landing-about.html'), name='landing_about'),
    url(r'^terms/$', TemplateView.as_view(template_name='visitor/terms.html'), name='website_terms'),
    url(r'^contact$', TemplateView.as_view(template_name='visitor/contact.html'), name='website_contact'),
    url(r'^topics/$', TemplateView.as_view(template_name='visitor/topics.html'), name='website_topics'),
    url(r'^categories/$', TemplateView.as_view(template_name='visitor/categories.html'), name='website_categories'),
    url(r'^explore/$', TemplateView.as_view(template_name='visitor/site_explore.html'), name='website_explore'),
    url(r'^resources/$', TemplateView.as_view(template_name='visitor/resources.html'), name='website_resources'),
    url(r'^webscrap/$', TemplateView.as_view(template_name='visitor/webscrap.html'), name='webscrap'),
    url(r'^misc/$', TemplateView.as_view(template_name='visitor/misc.html'), name='misc-scripts'),

    # Account management is done by allauth
    url(r'^accounts/', include('allauth.urls')),

    # Account profile and member info done locally
    # Located in views to use models\db
    url(r'^accounts/profile/$', account_profile, name='account_profile'),
    url(r'^question/$', index, name='all_questions'),
    url(r'^member/action$', member_action, name='user_action'),
    
    # This path WORKS to display choice-question. 
    path(r'question/newblog', new_blog_post, name='newblog'),
    path(r'question/<int:question_id>/', detail, name='detail'),
    path(r'question/<int:question_id>/vote/', vote, name='vote'),
    path(r'question/<int:question_id>/results', results, name='results'),

    # Usual Django admin
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

