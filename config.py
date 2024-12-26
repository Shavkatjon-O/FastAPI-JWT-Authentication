import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# database
POSTGRESQL_DB_URI = os.environ.get("POSTGRESQL_DB_URI")

# authentication
SECRET_KEY = "vSSjUkd6cLf7Gkt3z4ZBY6Lbr8U06uSwXg0auTZYpF3X74skruNYhPymIPBRHpcu"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
