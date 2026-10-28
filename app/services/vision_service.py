from fastapi import FastAPI

app = FastAPI()


@app.get("/vision/ready")
async def vision_ready() -> dict:
    return {
        "status": "ready",
        "module": "vision_service",
        "task": "detect landing zones and restaurant targets",
    }
