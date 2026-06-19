from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "Server Python 3 chạy trên Docker thành công!"
    }

@app.get("/ping")
def ping():
    return {"ping": "pong"}
