from itertools import chain
from traceback import format_exc

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest, STATUS_CODE_TEXT
from django.core.urlresolvers import RegexURLResolver
from django.http import Http404, HttpResponseNotFound, HttpResponse
from django.utils.html import escape


class wsgi_application(object):
    def __init__(self, function_or_urlconf):
        if not settings.configured:
            settings.configure()
        self.function_or_urlconf = function_or_urlconf

    def get_view(self, request):
        if isinstance(self.function_or_urlconf, list):
            return self.resolve_view(request)
        return self.function_or_urlconf, (), {}

    def resolve_view(self, request):
        urls = self.function_or_urlconf
        resolver = RegexURLResolver(r"^/", urls)
        return resolver.resolve(request.path_info)

    def __call__(self, environ, start_response):
        request = WSGIRequest(environ)
        try:
            view, args, kwargs = self.get_view(request)
            response = view(request, *args, **kwargs)
        except Http404:
            response = HttpResponseNotFound("Couldn't find %s" % escape(request.path_info))
        except Exception, e:
            response = HttpResponse(format_exc(e), status=500, mimetype="text/plain")
        status_text = STATUS_CODE_TEXT.get(response.status_code, "UNKOWN STATUS CODE")
        status = "%s %s" % (response.status_code, status_text)
        response_headers = [(str(k), str(v)) for k, v in response.items()]
        for c in response.cookies.values():
            response_headers.append(("Set-Cookie", str(c.output(header=""))))
        start_response(status, response_headers)
        return response


class ClosingIterator(object):
    def __init__(self, iterator, close_callback):
        self.iterator = iter(iterator)
        self.close_callback = close_callback

    def __iter__(self):
        return self

    def next(self):
        return self.iterator.next()

    def close(self):
        self.close_callback()

class django_view(object):
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, request):
        environ = request.environ
        results = {}
        buffer = []
        def start_response(status, response_headers, exc_info=None):
            if exc_info is not None:
                raise exc_info[0], exc_info[1], exc_info[2]
            results["status"] = status
            results["response_headers"] = response_headers
            return buffer.append
        response = self.wsgi_app(environ, start_response)
        while not results:
            buffer.append(response.next())
        response_iter = chain(buffer, response)
        if hasattr(response, "close"):
            response_iter = ClosingIterator(response_iter, response.close)
        response = HttpResponse(response_iter, status=int(results["status"].split()[0]))
        for header, value in results["response_headers"]:
            response[header] = value
        return response
