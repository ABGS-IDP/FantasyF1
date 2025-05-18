import uvicorn
import os

PORT = int(os.getenv("API_PORT", 8001))

if __name__ == "__main__":
    uvicorn.run("src.routes:app", host="0.0.0.0", port=PORT, reload=True)
