from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

MONGO_DB_URL = 'mongodb+srv://hr:hr@cluster0.aoqxdmb.mongodb.net/'
MONGO_DB_NAME = "FastAPI4"
location_collection_name = "Location"


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


class Location(BaseModel):
    city: str
    country_id: str
    postal: str


class LocationInDB(Location):
    id: str


@app.get("/locations", response_model=List[LocationInDB])
async def get_locations():
    await connect_to_mongo()
    db = await get_database()
    locations = await db[location_collection_name].find({}).to_list(None)
    return [LocationInDB(**location, id=str(location["_id"])) for location in locations]


@app.post("/locations", response_model=LocationInDB)
async def create_location(location: Location):
    db = await get_database()
    location_dict = location.dict()
    result = await db[location_collection_name].insert_one(location_dict)
    created_location = await db[location_collection_name].find_one({"_id": result.inserted_id})

    if created_location:
        return LocationInDB(**created_location, id=str(created_location["_id"]))
    else:
        raise HTTPException(status_code=500, detail="Failed to create Location")


@app.put("/locations/{location_id}", response_model=LocationInDB)
async def update_location(location_id: str, location: Location):
    db = await get_database()
    location_dict = location.dict()
    result = await db[location_collection_name].update_one(
        {"_id": ObjectId(location_id)},
        {"$set": location_dict}
    )

    if result.modified_count == 1:
        updated_location = await db[location_collection_name].find_one({"_id": ObjectId(location_id)})
        return LocationInDB(**updated_location, id=str(updated_location["_id"]))
    else:
        raise HTTPException(status_code=404, detail="Location not found")


@app.delete("/locations/{location_id}", response_model=dict)
async def delete_location_by_id(location_id: str):
    db = await get_database()

    existing_location = await db[location_collection_name].find_one({"_id": ObjectId(location_id)})
    if existing_location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    result = await db[location_collection_name].delete_one({"_id": ObjectId(location_id)})

    if result.deleted_count == 1:
        return {"message": f"Location with ID '{location_id}' deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the Location")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
