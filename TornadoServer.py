import datetime
from functools import wraps

import tornado.httpserver
import tornado.ioloop
import tornado.ioloop
import tornado.web
import tornado.web
import opentracing
from random import randint
from time import sleep
from opentracing import Tracer
from instana import options as o
import logging
import opentracing as ot
from instana import tracer
import time
import opentracing.ext.tags as ext


class MainHandler(tornado.web.RequestHandler):

	def initialize(self):
		SERVICE = "🦄 Stan ❤️s Python 🦄"
		tracer.init(o.Options(service=SERVICE, log_level=logging.DEBUG))
		print ("Calling initialize " + str(self) + str(SERVICE))
		today = datetime.datetime.now()
		print (today)
		self.tracer = Tracer()
		self.span = self.tracer.start_span(operation_name='root')
		self.span.set_tag('RequestHandler','MainHandler')
		self.requestmethod = ""
		self.clazzName = self.__class__.__name__

	def instana_span_decorator(orig_func):
		@wraps(orig_func)
		def wrapper(*args, **kwargs):
			print ("Before Call >> " )
			thisInstance = args[0]
			parent_span = opentracing.tracer.start_span(operation_name="DemoSpan")
			parent_span.set_tag(ext.COMPONENT, "Tornado")
			parent_span.set_tag(ext.SPAN_KIND, ext.SPAN_KIND_RPC_SERVER)
			parent_span.set_tag(ext.PEER_HOSTNAME, "localhost")
			parent_span.set_tag(ext.HTTP_URL, "/")
			parent_span.set_tag(ext.HTTP_METHOD, thisInstance.requestmethod)
			parent_span.set_tag(ext.HTTP_STATUS_CODE, 200)
			result = orig_func(*args, **kwargs)
			parent_span.finish()
			print (" << After Call")
			return result
		return wrapper

	@instana_span_decorator
	def get(self):
		self.requestmethod = "GET"
		print ("GET CALLED")
		self.write("<h1>Welcome to the Python Tracing</h1>")
		self.write("<hr></hr>")
		welcomeMessage = """Welcome to the Instana Python Sensor and Tracing Example. 
		The instana package provides Python metrics and traces (request, queue & cross-host) for Instana. Build Status OpenTracing Badge
		Note This package supports Python 2.7 or greater.
		Any and all feedback is welcome. Happy Python visibility. See the 
		<a href="https://github.com/instana/python-sensor">Python Sensor</a>
		Installation : pip install instana into the virtual-env or container (hosted on pypi)
		"""
		self.write(welcomeMessage)

	@instana_span_decorator
	def head(self):
		self.requestmethod = "HEAD"
		print ("HEAD CALLED")

	def post(self):
		self.requestmethod = "POST"
		print ("POST CALLED")
		self.write("<h1>THIS is a POST</h1>")

def make_app():
	return tornado.web.Application([
		(r"/", MainHandler),
	])

if __name__ == "__main__":
	app = make_app()
	portNumber = 8888
	app.listen(portNumber)
	print ("Starting Tornado Server on port " + str(portNumber))
	tornado.ioloop.IOLoop.current().start()
