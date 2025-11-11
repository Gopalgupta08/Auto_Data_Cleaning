import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/tmp')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16 MB
    ALLOWED_EXTENSIONS = {'csv'}