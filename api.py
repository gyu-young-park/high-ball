import inspect
from parse import parse
from webob import Request, Response
from requests import Session as RequestSession
from wsgiadapter import WSGIAdapter as RequestWSGIAdapter

class API:
    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)
    
    def test_session(self, base_url="http://testserver"):
        session = RequestSession()
        session.mount(prefix=base_url, adapter=RequestWSGIAdapter(self))
        return session
        
    def handle_request(self, request):
        response = Response()

        handler, kwargs = self._find_hadler(request_path=request.path)

        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    raise AttributeError("Method not allowed", request.method)
            
            handler(request, response, **kwargs)  
        else:
            self.default_response(response)
        return response

    def _find_hadler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        
        return None, None

    def route(self, path):
        if path in self.routes:
            raise AssertionError("Such route already exists.")
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        
        return wrapper
    
    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found"