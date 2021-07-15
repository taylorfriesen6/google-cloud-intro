from typing import Optional, Dict

from fastapi import FastAPI
from pydantic import BaseModel

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import google.cloud.logging

project_id = "tag-counter-319600"

app = FastAPI(openapi_tags=[
    {
        "name": "increment count",
        "description": "adds **value** to the current value stored for the tag **name**",
    },
    {
        "name": "get tag stats",
        "description": "returns the list of tags that have been passed in, and for each tag returns the sum of all the corresponding increment values"
    },
])

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})
db = firestore.client()

logger = google.cloud.logging.Client().logger("my-log")

class Tag(BaseModel):
    name: str = ""
    value: int = 0

@app.get("/", response_model = Dict[str, int], tags=["get tag stats"])
async def get_tag_stats():
    docs = db.collection(u'tags').stream()
    result = {}
    for doc in docs:
        result[doc.id] = doc.to_dict()[u'sum']
    return result

@app.post("/", tags=["increment count"])
async def increment_count(tag: Tag):
    name = tag.name
    value = tag.value
    log_data = {
        "operation": "increment count",
        "name": name,
        "value": value
    }
    logger.log_struct(log_data, severity="INFO")
    doc_ref = db.collection(u'tags').document(name)
    doc = doc_ref.get()
    if doc.exists:
        prior_sum = doc.to_dict()[u'sum']
        doc_ref.set({
            u'sum': prior_sum + value
        })
    else:
        doc_ref.set({
            u'sum': value
        })