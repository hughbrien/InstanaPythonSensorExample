import datetime
from functools import wraps

import tornado.httpserver
import tornado.ioloop
import tornado.ioloop
import tornado.web
import tornado.web
import opentracing
from opentracing import Tracer
from instana import options
from instana import tracer
import opentracing.ext.tags as tags
import logging


class MainHandler(tornado.web.RequestHandler):

	def initialize(self):
		SERVICE = "🦄 Stan ❤️s Python 🦄"
		tracer.init(options.Options(service=SERVICE, log_level=logging.DEBUG))
		print ("Calling initialize " + str(self) + str(SERVICE))
		today = datetime.datetime.now()
		print (today)
		self.tracer = Tracer()
		self.rootspan = self.tracer.start_span(operation_name='root')
		self.rootspan.set_tag('RequestHandler','MainHandler')
		self.requestmethod = ""
		self.clazzName = self.__class__.__name__

	def instana_span_decorator(orig_func):
		@wraps(orig_func)
		def wrapper(*args, **kwargs):
			print ("Before Call >> " )
			result = orig_func(*args, **kwargs)
			print (" << After Call")
			return result
		return wrapper

	@instana_span_decorator
	def get(self):
		self.requestmethod = "GET"
		parent_span = opentracing.tracer.start_span(operation_name="tornade-request")
		parent_span.set_tag(tags.COMPONENT, "Tornado")
		parent_span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
		parent_span.set_tag(tags.PEER_HOSTNAME, "localhost")
		parent_span.set_tag(tags.HTTP_URL, "/tornado")
		parent_span.set_tag(tags.HTTP_METHOD, "GET")
		parent_span.set_tag(tags.HTTP_STATUS_CODE, 200)
		status = self.__class__.get_status(self)
		request = self.request
		print(status)
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
		parent_span.finish()

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
