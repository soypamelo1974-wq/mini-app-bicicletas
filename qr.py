import qrcode
import uuid
from datetime import datetime, timedelta

def generate_qr(user_id):
    token = str(uuid.uuid4())
    expires = datetime.now() + timedelta(minutes=5)
    # Guardar en DB: userId, token, expires
    url = f"https://miapp.com/qr-login?token={token}"
    img = qrcode.make(url)
    img.save(f"qr_{user_id}.png")
    return url

