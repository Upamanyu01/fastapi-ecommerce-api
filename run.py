import uvicorn
from app.logger_config import logger

logger.info("Starting Ecommerce API server...")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True, log_config=None)
