from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

MONGO_DB_URL = 'mongodb+srv://hr:hr@cluster0.aoqxdmb.mongodb.net/'
MONGO_DB_NAME = "FastAPI4"
jobhistory_collection_name = "JobHistory"


class MongoDB:
    client: AsyncIOMotorClient = None


db = MongoDB()


async def get_database() -> AsyncIOMotorClient:
    return db.client[MONGO_DB_NAME]


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(MONGO_DB_URL)


async def close_mongo_connection():
    db.client.close()


app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


class JobHistory(BaseModel):
    employee_id: str
    job_title: str
    start_date: str
    end_date: str
    dep_id: str


class JobHistoryInDB(JobHistory):
    id: str


@app.get("/jobhistory", response_model=List[JobHistoryInDB])
async def get_jobhistory():
    await connect_to_mongo()
    db = await get_database()
    jobhistory = await db[jobhistory_collection_name].find({}).to_list(None)
    return [JobHistoryInDB(**job, id=str(job["_id"])) for job in jobhistory]


@app.post("/jobhistory", response_model=JobHistoryInDB)
async def create_jobhistory(jobhistory: JobHistory):
    db = await get_database()
    jobhistory_dict = jobhistory.dict()
    result = await db[jobhistory_collection_name].insert_one(jobhistory_dict)
    created_jobhistory = await db[jobhistory_collection_name].find_one({"_id": result.inserted_id})

    if created_jobhistory:
        return JobHistoryInDB(**created_jobhistory, id=str(created_jobhistory["_id"]))
    else:
        raise HTTPException(status_code=500, detail="Failed to create JobHistory")


@app.put("/jobhistory/{jobhistory_id}", response_model=JobHistoryInDB)
async def update_jobhistory(jobhistory_id: str, jobhistory: JobHistory):
    db = await get_database()
    jobhistory_dict = jobhistory.dict()
    result = await db[jobhistory_collection_name].update_one(
        {"_id": ObjectId(jobhistory_id)},
        {"$set": jobhistory_dict}
    )

    if result.modified_count == 1:
        updated_jobhistory = await db[jobhistory_collection_name].find_one({"_id": ObjectId(jobhistory_id)})
        return JobHistoryInDB(**updated_jobhistory, id=str(updated_jobhistory["_id"]))
    else:
        raise HTTPException(status_code=404, detail="JobHistory not found")


@app.delete("/jobhistory/{jobhistory_id}", response_model=dict)
async def delete_jobhistory_by_id(jobhistory_id: str):
    db = await get_database()

    existing_jobhistory = await db[jobhistory_collection_name].find_one({"_id": ObjectId(jobhistory_id)})
    if existing_jobhistory is None:
        raise HTTPException(status_code=404, detail="JobHistory not found")

    result = await db[jobhistory_collection_name].delete_one({"_id": ObjectId(jobhistory_id)})

    if result.deleted_count == 1:
        return {"message": f"JobHistory with ID '{jobhistory_id}' deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the JobHistory")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
