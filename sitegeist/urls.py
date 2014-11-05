from django.views.generic import TemplateView, RedirectView
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import Http404
from django.shortcuts import render

admin.autodiscover()


def justatemplate(path):
    def view(request):
        context = {
            "show_header": True,
            "data": {"data": "is fake"},
        }
        return render(request, path, context)
    return view


def share(request):

    valid_panes = ['people', 'housing', 'fun', 'environment', 'history']

    pane = request.GET.get('p', 'people')
    if pane not in valid_panes:
        raise Http404

    pane_url = "/api/%s/" % pane

    cll = request.GET.get('cll')
    if cll:
        pane_url = "%s?cll=%s" % (pane_url, cll)

    context = {"pane_url": pane_url}
    return render(request, "share.html", context)


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^404/$', justatemplate('404.html')),
    url(r'^500/$', justatemplate('500.html')),

    url(r'^api/', include('sitegeist.api.urls')),
    url(r'^dev/$', TemplateView.as_view(template_name='dev.html')),
    url(r'^geo/', include('boundaries.urls')),

    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^about/$', justatemplate('sitegeist/panes/methodology.html')),
    url(r'^share/$', share),

    url(r'^android/$', RedirectView.as_view(url='https://play.google.com/store/apps/details?id=com.sunlightfoundation.sitegeist.android')),
    url(r'^ios/$', RedirectView.as_view(url='https://itunes.apple.com/us/app/sitegeist/id582687408?ls=1&mt=8')),
    url(r'^kickstarter/$', RedirectView.as_view(url='https://kickstarter.com')),
)
