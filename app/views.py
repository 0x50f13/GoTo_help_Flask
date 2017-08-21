from app import site

@site.route('/')
def show_entries():
    return '200 ok'