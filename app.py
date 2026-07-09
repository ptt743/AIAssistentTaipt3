from fastapi import FastAPI, Request
import requests
import threading
app = FastAPI()

ZALO_ACCESS_TOKEN = '3963325544432664358:LmvKzdOsOcQGHOqlabTisFDCldhBsNqbIpZjausvWwbYjlBHlTMJNtjWHYqAhIis'
ZALO_BOT_TOKEN = os.environ.get("ZALO_BOT_TOKEN",ZALO_ACCESS_TOKEN)
BASE_URL = f"https://bot-api.zapps.me/bot{ZALO_BOT_TOKEN}"

def send_message(chat_id, text):
    """Gửi tin nhắn trả lời cho người dùng qua Zalo Bot API.
 
    Đây chính là cách 'trả response về cho bot': gọi endpoint sendMessage,
    KHÔNG phải trả nội dung trong HTTP response của webhook.
    """
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"Đã gửi tin phản hồi thành công tới {chat_id}")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gửi API Zalo: {e}")
        if e.response is not None:
            print("Chi tiết lỗi từ Zalo:", e.response.text)

def process_message(update):
    """Xử lý một update và gửi câu trả lời.
 
    Cấu trúc update của Zalo Bot API (giống Telegram):
    {
        "message": {
            "text": "...",
            "chat": {"id": "..."},
            "from": {...}
        }
    }
    """
    message = update.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    user_message = (message.get("text") or "").strip()
 
    if not chat_id or not user_message:
        return
 
    print(f'Nhận được tin nhắn: "{user_message}" từ chat_id: {chat_id}')
 
    # Xử lý logic Backend (kiểm tra giờ giấc, query Database...)
    reply_text = "Dạ, hệ thống đã ghi nhận thông tin."
 
    if "đặt món" in user_message.lower():
        reply_text = (
            "Dạ buổi tối bên em đang có sẵn Bún Bò Huế và Cơm Tấm. "
            "Anh muốn dùng món nào ạ? (Anh có thể ghi chú thêm như không hành, ít cay...)"
        )
 
    send_message(chat_id, reply_text)

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

    thread = threading.Thread(target=process_message, args=(data,))
    thread.start()
    
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
