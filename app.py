import os
import threading

import requests
from fastapi import FastAPI, Request

app = FastAPI()

# QUAN TRỌNG: đặt token trong biến môi trường trên Render (tab Environment),
# tên biến: ZALO_BOT_TOKEN. KHÔNG hardcode token vào code.
ZALO_BOT_TOKEN = os.environ.get("ZALO_BOT_TOKEN", "DAN_TOKEN_CUA_BAN_VAO_DAY")
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
        "message": "Server Zalo Bot chạy trên Docker thành công!",
    }


@app.post("/webhook")
async def zalo_webhook(request: Request):
    # Lấy dữ liệu Zalo gửi về
    data = await request.json()
    print("Dữ liệu Zalo gửi về:", data)

    # Zalo Bot API bọc dữ liệu update trong khóa "result".
    update = data.get("result", data)

    # Xử lý bất đồng bộ để trả 200 về cho Zalo thật nhanh
    threading.Thread(target=process_message, args=(update,)).start()

    # BẮT BUỘC: chỉ cần trả HTTP 200 để báo đã nhận.
    return {"ok": True}


@app.get("/ping")
def ping():
    return {"ping": "pong"}
