from bottle import route, default_app


@route('/')
def home():
    """Home page."""
    return 'home'


@route('/<user>')
def user(user):
    """User profile page.

    :param user: user login name
    :status 200: when user exists
    :status 404: when user doesn't exist

    """
    return 'hi, ' + user


@route('/<user>/posts/<post_id:int>')
def post(user, post_id):
    """User's post.

    :param user: user login name
    :param post_id: post unique id
    :status 200: when user and post exists
    :status 404: when user and post doesn't exist

    """
    return str(post_id), 'by', user


app = default_app()
