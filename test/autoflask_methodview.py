from flask import Flask
from flask.views import MethodView


app = Flask(__name__)


class UserView(MethodView):
    def get(self, user):
        """Shows profile page.

        :param user: user login name
        :status 200: when user exists
        :status 404: when user doesn't exist
        """
        return 'hi, ' + user

    def patch(self, user):
        """Modifies profile.

        :param user: success
        """
        return '', 204


app.add_url_rule('/v1/user/<user>', 'user_v1', UserView.as_view('user_v1'))
app.add_url_rule('/v2/user/<user>', 'user_v2', UserView.as_view('user_v2'))
