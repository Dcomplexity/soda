from urls import urls

import tornado.web
import os

SETTINGS = dict(
template_path = os.path.join(os.path.dirname(__file__), "templates"),
static_path = os.path.join(os.path.dirname(__file__), "static"),
cookie_secret = "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo="
)

application = tornado.web.Application(
	handlers = urls,
	**SETTINGS
)