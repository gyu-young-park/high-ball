from api import API
from middleware import Middleware

app = API()

print("temp !3232")

@app.route("/home")
def home(request, response):
    print(request.method)
    if request.method == 'GET':
        response.text = "Hello from the HOME page"
    else:
        raise AttributeError("Method not allowed")

@app.route("/about", allowed_methods=["get", "post"])
def about(request, response):
    response.text = "Hello from the ABOUT page"

@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"

@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"
        
    def post(self, req, resp):
        resp.text = "Endpoint to create a book"

@app.route("/exception")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be used.")

@app.route("/template")
def template_handler(req, resp):
    resp.html = app.template("index.html", context={
        "name": "gyu",
        "title": "Best Framework"
    })
    
@app.route("/json")
def json_handler(req , resp):
    resp.json = {"name": "data", "type": "JSON"}
    
@app.route("/text")
def text_handler(req ,resp):
    resp.text = "This is a simple text"


def handler(req, resp):
    resp.text = "sample"

app.add_route("/sample", handler)

def custom_exception_handler(request, response, exception_cls):
    response.text = str(exception_cls)

app.add_exception_handler(custom_exception_handler)

class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)
    
    def process_response(self, req, resp):
        print("Processing response", req.url)
        
app.add_middleware(SimpleCustomMiddleware)