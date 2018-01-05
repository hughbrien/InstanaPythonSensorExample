import datetime
from functools import wraps
import tornado.httpserver
import tornado.ioloop
import tornado.ioloop
import tornado.web
import tornado.web
import opentracing
from opentracing import Tracer
from instana import options as o
import logging
from instana import tracer

import opentracing.ext.tags as ext

class MainHandler(tornado.web.RequestHandler):

	def initialize(self):
		SERVICE = "🦄 Stan ❤️s Python 🦄"
		tracer.init(o.Options(service=SERVICE, log_level=logging.DEBUG))
		print("Calling initialize " + str(self) + str(SERVICE))
		today = datetime.datetime.now()
		print(today)
		self.tracer = Tracer()
		self.span = self.tracer.start_span(operation_name='root')
		self.requestmethod = ""
		self.clazzName = self.__class__.__name__
		self.span.set_tag('RequestHandler', self.clazzName)

	def instana_span_decorator(orig_func):
		@wraps(orig_func)
		def wrapper(*args, **kwargs):
			requestObject = None
			print("Before Call >> ")
			requestObject = args[0]
			if requestObject is not None:
				spanName = requestObject.clazzName
				print("Request Object is NOT None")
				print(requestObject)
				decorator_http_method = requestObject.request.method
				decorator_http_host = requestObject.request.host
				decorator_http_path = requestObject.request.path
				decorator_http_url = requestObject.request.path
				decorator_http_requesttime = requestObject.request.request_time()
				print("Request Object")
				print(decorator_http_method)
				parent_span = opentracing.tracer.start_span(operation_name=spanName)
				parent_span.set_tag(ext.COMPONENT, "Tornado Request Handler")
				parent_span.set_tag(ext.SPAN_KIND, ext.SPAN_KIND_RPC_SERVER)
				parent_span.set_tag(ext.PEER_HOSTNAME, decorator_http_host)
				parent_span.set_tag(ext.HTTP_URL, decorator_http_path)
				parent_span.set_tag(ext.HTTP_METHOD, decorator_http_method)
				parent_span.set_tag(ext.HTTP_STATUS_CODE, 200)
				parent_span.set_tag("RequestTime", decorator_http_requesttime)
				result = orig_func(*args, **kwargs)
				parent_span.finish()
			else:
				print("help")
				parent_span = opentracing.tracer.start_span(operation_name="DemoSpan")
				parent_span.set_tag(ext.COMPONENT, "Tornado")
				parent_span.set_tag(ext.SPAN_KIND, ext.SPAN_KIND_RPC_SERVER)
				parent_span.set_tag(ext.PEER_HOSTNAME, "localhost")
				parent_span.set_tag(ext.HTTP_URL, "/")
				parent_span.set_tag(ext.HTTP_METHOD, "GET")
				parent_span.set_tag(ext.HTTP_STATUS_CODE, 404)
				result = orig_func(*args, **kwargs)
				parent_span.finish()
			print(" << After Call")
			return result
		return wrapper

	@instana_span_decorator
	def get(self):
		self.requestmethod = "GET"
		print("GET CALLED")
		self.write("<html><head><title>Python Tracing Demo</title></head><body>")
		self.write("<h1>Welcome to the Python Tracing</h1>")
		self.write("<hr></hr>")
		welcomeMessage = """Welcome to the Instana Python Sensor and Tracing Example. 
		The instana package provides Python metrics and traces (request, queue & cross-host) for Instana. Build Status OpenTracing Badge
		Note This package supports Python 2.7 or greater.
		Any and all feedback is welcome. Happy Python visibility. See the 
		<a href="https://github.com/instana/python-sensor">Python Sensor</a>
		Installation : pip install instana into the virtual-env or container (hosted on pypi)
		"""
		localheaders = self.request.headers
		myHost = localheaders["Host"]
		userAgent = localheaders["User-Agent"]
		connection = localheaders["Connection"]
		cacheControl = localheaders["Cache-Control"]
		referrer = localheaders["Referer"]
		self.write(welcomeMessage)
		self.write("<ul>")
		self.write("<li>")
		self.write(myHost)
		self.write("<li>")
		self.write(userAgent)
		self.write("<li>")
		self.write(connection)
		self.write("<li>")
		self.write(referrer)
		self.write("<li>")
		self.write(self.request.uri)
		self.write("<li>")
		self.write(self.request.path)
		self.write("<li>")
		self.write(self.request.query)
		self.write("<li>")
		self.write(self.request.version)
		self.write("<li>")
		self.write(self.request.protocol)
		self.write("<li>")
		self.write(self.request.host)
		self.write("</ul>")
		self.write(str(self.request.headers))
		self.write("</body></html>")
		print("GET ENDED")

	@instana_span_decorator
	def head(self):
		self.requestmethod = "HEAD"
		print("HEAD CALLED")

	def post(self):
		self.requestmethod = "POST"
		print("POST CALLED")
		self.write("<h1>THIS is a POST</h1>")

	def prepare(self):
		print("Called Prepare")

	def on_finish(self):
		print("Called Finish")

class HomeHandler(tornado.web.RequestHandler):
	def initialize(self):
		SERVICE = "Home Handler"
		tracer.init(o.Options(service=SERVICE, log_level=logging.DEBUG))
		print("Calling initialize " + str(self) + str(SERVICE))
		today = datetime.datetime.now()
		print(today)
		self.tracer = Tracer()
		self.span = self.tracer.start_span(operation_name='root')
		self.requestmethod = ""
		self.clazzName = self.__class__.__name__
		self.span.set_tag('RequestHandler', self.clazzName)

	def instana_span_decorator(orig_func):
		@wraps(orig_func)
		def wrapper(*args, **kwargs):
			requestObject = None
			print("Before Call >> ")
			requestObject = args[0]
			if requestObject is not None:
				spanName = requestObject.clazzName
				print("Request Object is NOT None")
				print(requestObject)
				decorator_http_method = requestObject.request.method
				decorator_http_host = requestObject.request.host
				decorator_http_path = requestObject.request.path
				decorator_http_url = requestObject.request.path
				decorator_http_requesttime = requestObject.request.request_time()
				print("Request Object")
				print(decorator_http_method)
				parent_span = opentracing.tracer.start_span(operation_name=spanName)
				parent_span.set_tag(ext.COMPONENT, "Tornado Request Handler")
				parent_span.set_tag(ext.SPAN_KIND, ext.SPAN_KIND_RPC_SERVER)
				parent_span.set_tag(ext.PEER_HOSTNAME, decorator_http_host)
				parent_span.set_tag(ext.HTTP_URL, decorator_http_path)
				parent_span.set_tag(ext.HTTP_METHOD, decorator_http_method)
				parent_span.set_tag(ext.HTTP_STATUS_CODE, 200)
				parent_span.set_tag("RequestTime", decorator_http_requesttime)
				result = orig_func(*args, **kwargs)
				parent_span.finish()
			else:
				print("help")
				parent_span = opentracing.tracer.start_span(operation_name="DemoSpan")
				parent_span.set_tag(ext.COMPONENT, "Tornado")
				parent_span.set_tag(ext.SPAN_KIND, ext.SPAN_KIND_RPC_SERVER)
				parent_span.set_tag(ext.PEER_HOSTNAME, "localhost")
				parent_span.set_tag(ext.HTTP_URL, "/")
				parent_span.set_tag(ext.HTTP_METHOD, "GET")
				parent_span.set_tag(ext.HTTP_STATUS_CODE, 404)
				result = orig_func(*args, **kwargs)
				parent_span.finish()
			print(" << After Call")
			return result
		return wrapper

	@instana_span_decorator
	def get(self):
		self.write("Get Try")

	@instana_span_decorator
	def post(self):
		self.write("Post Try")

def make_app():
	return tornado.web.Application([
		(r"/", MainHandler),
		(r"/demo", HomeHandler),
	])

if __name__ == "__main__":
	app = make_app()
	portNumber = 8888
	app.listen(portNumber)
	print("Starting Tornado Server on port " + str(portNumber))
	tornado.ioloop.IOLoop.current().start()
