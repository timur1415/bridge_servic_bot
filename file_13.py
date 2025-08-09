from typing import Union
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/scan_user/{user_email}")
async def scan_user(item_id: int, q: Union[str, None] = None):
    ...
    # return {"item_id": item_id, "q": q}
