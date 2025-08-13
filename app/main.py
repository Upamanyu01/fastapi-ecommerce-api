from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from .logger_config import logger
from .routers import auth_routes, brand_routes, category_routes, subcategory_routes, product_routes

app = FastAPI(title="Ecommerce API")

# Include routers
app.include_router(auth_routes.router)
app.include_router(brand_routes.router)
app.include_router(category_routes.router)
app.include_router(subcategory_routes.router)
app.include_router(product_routes.router)

# Middleware to log all requests and responses
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")

        try:
            body = await request.json()
            logger.info(f"Request Body: {body}")
        except Exception:
            pass  # Not all requests have JSON body

        response = await call_next(request)
        logger.info(f"Response Status: {response.status_code}")
        return response

app.add_middleware(LoggingMiddleware)
