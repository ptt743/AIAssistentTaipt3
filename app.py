from fastapi import FastAPI, Request
app = FastAPI()

ZALO_ACCESS_TOKEN = '3963325544432664358:LmvKzdOsOcQGHOqlabTisFDCldhBsNqbIpZjausvWwbYjlBHlTMJNtjWHYqAhIis'


def send_zalo_message(user_id, text):
    endpoint = 'https://openapi.zalo.me/v3.0/oa/message/cs'
    
    # Đóng gói data theo đúng format Zalo yêu cầu
    payload = {
        "recipient": {
            "user_id": user_id
        },
        "message": {
            "text": text
        }
    }
    
    headers = {
        'access_token': ZALO_ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status() # Kiểm tra xem request có lỗi HTTP không
        print(f"Đã gửi tin phản hồi thành công tới {user_id}")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gửi API Zalo: {e}")
        if e.response is not None:
            print("Chi tiết lỗi từ Zalo:", e.response.json())

def process_message(body):
    if body.get('event_name') == 'user_send_text':
        user_id = body['sender']['id']
        user_message = body['message']['text']

        print(f'Nhận được tin nhắn: "{user_message}" từ user: {user_id}')

        # Xử lý logic Backend (Ví dụ: kiểm tra giờ giấc, query Database...)
        reply_text = "Dạ, hệ thống đã ghi nhận thông tin."
        
        if "đặt món" in user_message.lower():
            # Giả lập bot trả lời dựa trên logic
            reply_text = "Dạ buổi tối bên em đang có sẵn Bún Bò Huế và Cơm Tấm. Anh muốn dùng món nào ạ? (Anh có thể ghi chú thêm như không hành, ít cay...)"

        # Gọi hàm gửi tin đi
        send_zalo_message(user_id, reply_text)


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

    thread = threading.Thread(target=process_message, args=(body,))
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
