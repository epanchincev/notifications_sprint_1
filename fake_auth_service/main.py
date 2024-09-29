from enum import Enum

from fastapi import FastAPI

app = FastAPI()


class AuthServiceField(Enum):
    USER_NAME = "user_name"
    EMAIL = "email"



@app.get('/api/v1/user/{user_id}')
async def get_user(user_id: str):
    random_user = {
        AuthServiceField.USER_NAME.value: f"user_{user_id}",
        AuthServiceField.EMAIL.value: f"user{user_id}@example.com"
    }

    return random_user
