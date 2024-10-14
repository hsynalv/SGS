import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasındaki değişkenleri yükler

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
