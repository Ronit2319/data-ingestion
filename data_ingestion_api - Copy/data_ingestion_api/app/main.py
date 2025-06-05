from fastapi import FastAPI, BackgroundTasks
from uuid import uuid4
from .models import IngestionRequest, Batch, BatchStatus
from .storage import ingestions, priority_queues
from .processor import process_batches

import asyncio

app = FastAPI()
started = False

@app.on_event("startup")
async def start_background_processor():
    global started
    if not started:
        asyncio.create_task(process_batches())
        started = True

@app.post("/ingest")
async def ingest(req: IngestionRequest):
    ingestion_id = str(uuid4())
    batches = [Batch(req.ids[i:i + 3]) for i in range(0, len(req.ids), 3)]
    ingestions[ingestion_id] = {
        "status": "yet_to_start",
        "priority": req.priority,
        "created_at": datetime.utcnow(),
        "batches": batches
    }

    for batch in batches:
        priority_queues[req.priority].append((ingestion_id, batch))

    return {"ingestion_id": ingestion_id}

@app.get("/status/{ingestion_id}")
async def status(ingestion_id: str):
    if ingestion_id not in ingestions:
        return {"error": "Ingestion ID not found"}

    ingestion = ingestions[ingestion_id]
    batch_list = [{
        "batch_id": batch.batch_id,
        "ids": batch.ids,
        "status": batch.status
    } for batch in ingestion["batches"]]

    return {
        "ingestion_id": ingestion_id,
        "status": ingestion["status"],
        "batches": batch_list
    }
