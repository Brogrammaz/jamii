from fastapi import FastAPI
from jamii.api.routes import user, deposits, loan
from loguru import logger
from jamii import auth  # Import the route files


# configure Loguru to log to a file with rotation
logger.add("jamii.log", rotation="1 MB")


app = FastAPI()

app.include_router(user.router)
app.include_router(loan.router, prefix="/api")
app.include_router(deposits.router, prefix="/api")
app.include_router(auth.router)

# Basic root endpoint
@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Karibu Mwana-jamii"}


