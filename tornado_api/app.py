import tornado.ioloop
import tornado.web
from tornado.options import define, options

from opentelemetry import trace
from opentelemetry.instrumentation.tornado import TornadoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
#import requests

# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

define("port", default=8000, help="port to listen on")

TornadoInstrumentor().instrument()
RequestsInstrumentor().instrument()

class Handler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello!")


if __name__ == "__main__":
    app = tornado.web.Application([(r"/", Handler)])
    app.listen(options.port)

    print(f"Listening on http://localhost:{options.port}")
    tornado.ioloop.IOLoop.current().start()