import json
import os
from datetime import datetime

# تحديد المسار النسبي لملف الرسائل
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MESSAGES_DIR = os.path.join(BASE_DIR, "communication_hub", "messages")
MESSAGES_FILE = os.path.join(MESSAGES_DIR, "log.txt")

def send_message(sender, title, subject, content):
    """
    يرسل رسالة وينشئ المجلد والملف إذا لم يكونا موجودين.
    """
    os.makedirs(MESSAGES_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"--- MESSAGE START ---\n"
    message += f"Date: {timestamp}\n"
    message += f"Sender: {sender}\n"
    message += f"Title: {title}\n"
    message += f"Subject: {subject}\n"
    message += f"Content: {content}\n"
    message += f"--- MESSAGE END ---\n\n"
    
    with open(MESSAGES_FILE, "a", encoding='utf-8') as f:
        f.write(message)
    return f"Message sent from {sender} at {timestamp}"

def read_messages():
    """
    يقرأ الرسائل أو يعيد رسالة تفيد بعدم وجودها.
    """
    if not os.path.exists(MESSAGES_FILE):
        return "No messages yet. The system will create the file when the first message is sent."
    with open(MESSAGES_FILE, "r", encoding='utf-8') as f:
        return f.read()
