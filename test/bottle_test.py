
import unittest

from sphinxcontrib.autohttp.bottle import get_routes

from bottle import Bottle, Route


def create_app():
    app = Bottle()

    @app.route("/bottle")
    def bottle_bottle():
        return 12

    @app.post("/bottle/post/")
    def bottle_bottle_post():
        return 23

    return app


def create_app_mount():
    app = create_app()
    another_app = Bottle()

    @another_app.route("/mount/")
    def another_mount():
        pass

    app.mount("/mount/", another_app)
    return app


def create_app_filter():
    app = Bottle()

    @app.route("/hello/<name>")
    def bottle_hello_name(name):
        return name

    return app


class BottleTest(unittest.TestCase):

    def test_get_routes(self):
        routes = list(get_routes(create_app()))
        # order is not deterministic:
        routes = sorted(routes, key=lambda x: x[1])

        self.assertEqual(len(routes), 2)

        self.assertEqual(len(routes[0]), 3)
        self.assertEqual(routes[0][0], "GET")
        self.assertEqual(routes[0][1], "/bottle")
        self.assertEqual(routes[0][2].callback(), 12)
        self.assertEqual(type(routes[0][2]), Route)

        self.assertEqual(len(routes[1]), 3)
        self.assertEqual(routes[1][0], "POST")
        self.assertEqual(routes[1][1], "/bottle/post/")
        self.assertEqual(routes[1][2].callback(), 23)
        self.assertEqual(type(routes[1][2]), Route)

    def test_get_routes_mount(self):
        routes = list(get_routes(create_app_mount()))
        routes = sorted(routes, key=lambda x: x[1])

        self.assertEqual(len(routes), 3)

        # not sure about this:
        self.assertEqual(routes[2][1], "/mount/(:re:.*)")

    def test_get_routes_filter(self):
        routes = list(get_routes(create_app_filter()))
        routes = sorted(routes, key=lambda x: x[1])

        self.assertEqual(len(routes), 1)

        self.assertEqual(routes[0][1], "/hello/(name)")
