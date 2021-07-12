from typing import Optional, Dict

from fastapi import FastAPI
from pydantic import BaseModel

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})

db = firestore.client()


app = FastAPI()

class Tag(BaseModel):
    name: Optional[str] = None
    value: int = 0

@app.get("/", response_model = Dict[str, int])
async def read_all():
    docs = db.collection(u'tags').stream()
    result = {}
    for doc in docs:
        result[doc.id] = doc.to_dict()[u'sum']
    return result

@app.post("/")
async def increment_tag(tag: Tag):
    name = tag.name
    value = tag.value
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