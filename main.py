from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import traceback

# Configure logging
logging.basicConfig(
    filename="application.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

# Add exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error("Unhandled exception: %s", traceback.format_exc().replace("\n", " "))
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred."},
    )

# Include the router
from routers import example_router
app.include_router(example_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
