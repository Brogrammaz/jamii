from fastapi import FastAPI
from jamii.api.routes import user, deposits
from loguru import logger


# configure Loguru to log to a file with rotation
logger.add("jamii.log", rotation="1 MB")


app = FastAPI()

app.include_router(user.router)

app.include_router(deposits.router, prefix="/api")


# Basic root endpoint
@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Karibu Mwana-jamii"}


