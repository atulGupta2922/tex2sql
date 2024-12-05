from fastapi import FastAPI

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck():
    """
    Healthcheck route to verify the service is running.
    Returns a JSON response with status.
    """
    return {"status": "ok"}