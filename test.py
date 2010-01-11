from django.conf.urls.defaults import patterns
from django.http import HttpResponse

from django_wsgi import wsgi_application, django_view


def test_app(request):
    return HttpResponse("Hello World!")

def test_app2(request, name):
    return HttpResponse("Hello %s!" % name)

def test_app3(request):
    return HttpResponse("wowa, meta")

def test_app4(environ, start_response):
    start_response("200 OK", [("Content-type", "text/html")])
    yield "i suck"


urls = patterns("",
    (r"^$", test_app),
    (r"^meta/$", django_view(wsgi_application(test_app3))),
    (r"^test4/$", django_view(test_app4)),
    (r"^(?P<name>.*?)/$", test_app2),
)

application = wsgi_application(urls)
