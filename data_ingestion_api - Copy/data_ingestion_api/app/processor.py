import asyncio
from datetime import datetime
from .storage import ingestions, priority_queues
from .models import BatchStatus, Priority, Batch

BATCH_SIZE = 3
RATE_LIMIT_SECONDS = 5

async def process_batches():
    while True:
        for priority in [Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
            if priority_queues[priority]:
                ingestion_id, batch = priority_queues[priority].pop(0)
                batch.status = BatchStatus.TRIGGERED
                await asyncio.sleep(0)  # yield control

                # Update status
                ingestions[ingestion_id]["status"] = "triggered"
                await simulate_external_api(batch)

                batch.status = BatchStatus.COMPLETED

                # Check if all batches are complete
                batches = ingestions[ingestion_id]["batches"]
                if all(b.status == BatchStatus.COMPLETED for b in batches):
                    ingestions[ingestion_id]["status"] = "completed"

                await asyncio.sleep(RATE_LIMIT_SECONDS)
                break
        else:
            await asyncio.sleep(1)

async def simulate_external_api(batch):
    await asyncio.sleep(1)  # Simulate fetch delay
    # Mock data processing here
