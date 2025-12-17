from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import time

trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "calculation-service"}))
)

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger-agent",
    agent_port=6831,
)

trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)


@app.get("/")
def calculate():
    with trace.get_tracer(__name__).start_as_current_span("calculate_price"):
        time.sleep(0.1)
        return "Price calculated: 15000 RUB"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
