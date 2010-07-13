from bottle import route, run

@route('/')
def hello_world():
        return 'Hello World!'

run(host='localhost', port=8080)
