from fastapi import FastAPI, Request
app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "Server Python 3 chạy trên Docker thành công!"
    }

@app.post("/webhook")
async def zalo_webhook(request: Request):
    # Lấy dữ liệu Zalo gửi về
    data = await request.json()
    
    # In ra log để bạn xem trên Render
    print("Dữ liệu Zalo gửi về:", data)
    
    # Kiểm tra xem có phải sự kiện người dùng gửi tin nhắn không
    event_name = data.get("event_name")
    
    if event_name == "user_send_text":
        sender_id = data.get("sender", {}).get("id")
        text_message = data.get("message", {}).get("text", "")
        
        print(f"Người dùng {sender_id} vừa nhắn: {text_message}")
        # Ở đây bạn có thể thêm code xử lý AI hoặc logic của bạn
        
    # Bắt buộc: Phải trả về HTTP status 200 để báo cho Zalo là server đã nhận được
    return {"error": 0, "message": "Success"}

@app.get("/ping")
def ping():
    return {"ping": "pong"}
