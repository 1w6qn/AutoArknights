from bottle import *
@route("/")
@route("/index.html")
def index():return "hello world"
run()