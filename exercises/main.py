import random

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


class TaskBody(BaseModel):
    description: str
    priority: int | None = None  # default option
    is_complete: bool = False


class UserBody(BaseModel):
    username: str
    password: str
    is_admin: bool = False


app = FastAPI()

tasks_data = [
    {"id": 1, "description": "Learn FastAPI", "priority": 3, "is_complete": True},
    {"id": 2, "description": "Do exercises", "priority": 2, "is_complete": False}
]

users_data = [
    {"id": 1, "username": "Andrzej", "password": "qwerty123", "is_admin": True},
    {"id": 2, "username": "Andżela", "password": "hasło1!", "is_admin": False}
]


def get_item_by_id(items_list, id_):

    for item in items_list:
        if item["id"] == id_:
            result = item
            break
    else:
        result = None

    return result


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/tasks")
def get_tasks():
    return {"result": tasks_data}


@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    target_task = get_item_by_id(tasks_data, task_id)

    if not target_task:
        message = {"error": f"Task with id {task_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return {"result": target_task}


@app.get("/users")
def get_users():
    return {"result": users_data}


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    target_user = get_item_by_id(users_data, user_id)

    if not target_user:
        message = {"error": f"User with id {user_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return {"result": target_user}


@app.post("/tasks")
def create_task(body: TaskBody):  # type annotations + Ellipsis (...)

    new_task = body.model_dump()  # dict
    random_id = random.randint(1, 10000)
    new_task["id"] = random_id
    tasks_data.append(new_task)

    return {"message": "New task added", "details": new_task}


@app.post("/users")
def create_user(body: UserBody):

    new_user = body.model_dump()
    random_id = random.randint(1, 10000)
    new_user["id"] = random_id
    users_data.append(new_user)

    return {"message": "New user added", "details": new_user}
