from app import site

@site.route('/')
def index():
    return '200 ok'