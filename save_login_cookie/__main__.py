from dotenv import load_dotenv
import os
from .save_login_cookie import save_login_cookie

load_dotenv()

if __name__ == '__main__':
    try:
        email = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')
        res = save_login_cookie(email, password)
    except Exception as e:
        print(e)
