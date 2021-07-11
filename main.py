from typing import Optional, Dict

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Tag(BaseModel):
    name: Optional[str] = None
    value: int = 0

# currently storing data in memory!!
# this will result in data being lost whenever the service shuts down
# change this to firestore asap
tags = {"foo": 3}

@app.get("/", response_model = Dict[str, int])
async def read_all():
    return tags

@app.post("/")
async def increment_tag(tag: Tag):
    name = tag.name
    value = tag.value
    if name in tags:
        tags[name] += value
    else:
        tags[name] = value
    return tags