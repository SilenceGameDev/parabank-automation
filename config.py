import os
from dotenv import load_dotenv
from models import User

load_dotenv()

MY_TEST_USER = User(
    username=os.getenv("PARABANK_TEST_USERNAME"),
    password=os.getenv("PARABANK_TEST_PASSWORD"),
)

TEST_FIRST_NAME = "fname"
TEST_LAST_NAME = "lname"