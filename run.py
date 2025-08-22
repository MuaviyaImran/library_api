import uvicorn

from app.core.config import Config

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=Config.API_PORT, reload=True)
