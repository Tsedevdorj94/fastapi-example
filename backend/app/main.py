import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.main import api_router
from app.core.config import settings
from app.webhooks import send_webhook
import traceback as tb

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

async def global_exception_handler(request: Request, exc: Exception):
    # Capture the full exception traceback as a string
    print(f"Exception occurred: {exc} HELLOO####")
    trace = "".join(tb.format_exception(type(exc), exc, exc.__traceback__))
    print(trace)  # Log to console

    # EXAMPLE: send to webhook/LLM (pseudo-code)
    await send_webhook(trace)  # You need to implement this!

    return JSONResponse(status_code=500, content={"detail": "Internal error debugging suggestion sent by lambda."})

app.add_exception_handler(Exception, global_exception_handler)