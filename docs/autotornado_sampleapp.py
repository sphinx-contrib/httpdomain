from tornado.web import Application, RequestHandler, url


class MainHandler(RequestHandler):
    def get(self):
        """Home page."""
        self.write('home')


class UserHandler(RequestHandler):
    def get(self, user):
        """User profile page.

        :param user: user login name
        :status 200: when user exists
        :status 404: when user doesn't exist

        """
        return 'hi, ' + user


class UserPostHandler(RequestHandler):
    def get(user, post_id):
        """User's post.

        :param user: user login name
        :param post_id: post unique id
        :status 200: when user and post exists
        :status 404: when user and post doesn't exist

        """
        return str(post_id), 'by', user

app = Application([
    url(r'/', MainHandler),
    url(r'/(?P<user>[a-z0-9]+)', UserHandler),
    url(r'/(?P<user>[a-z0-9]+)/posts/(?P<post_id>[\d+]+)', UserPostHandler),
])
