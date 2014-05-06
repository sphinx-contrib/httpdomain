
import unittest

from sphinxcontrib.autohttp.bottle import get_routes

from bottle import Bottle, Route
app = Bottle()


@app.route("/bottle")
def bottle_bottle():
    pass


@app.post("/bottle/post/")
def bottle_bottle_post():
    pass


class BottleTest(unittest.TestCase):

    def test_get_routes(self):
        routes = list(get_routes(app))
        routes = sorted(routes)  # order is not deterministic
        self.assertEqual(routes[0][0], "GET")
        self.assertEqual(routes[0][1], "/bottle")
        self.assertEqual(routes[0][2].callback, bottle_bottle)
        self.assertEqual(type(routes[0][2]), Route)

        self.assertEqual(routes[1][0], "POST")
        self.assertEqual(routes[1][1], "/bottle/post/")
        self.assertEqual(routes[1][2].callback, bottle_bottle_post)
        self.assertEqual(type(routes[1][2]), Route)
