from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

MONGO_DB_URL = 'mongodb+srv://hr:hr@cluster0.aoqxdmb.mongodb.net/'
MONGO_DB_NAME = "FastAPI3"
appinsights_collection_name = "AppInsights"  # Modified
application_collection_name = "Application"  # Modified
process_collection_name = "Process"  # Modified


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


class AppInsights(BaseModel):  # Modified
    Appname: str
    ClientID: str
    Cluster: str
    ProcessName: str


class AppInsightsInDB(AppInsights):  # Modified
    id: str


class Application(BaseModel):  # Modified
    Appname: str
    Apptype: str
    Description: str


class ApplicationInDB(Application):  # Modified
    id: str


class Process(BaseModel):  # Modified
    ProcessName: str
    ProcessDescription: str
    Appname: str


class ProcessInDB(Process):  # Modified
    id: str


@app.get("/appinsights", response_model=List[AppInsightsInDB])  # Modified
async def get_appinsights():  # Modified
    await connect_to_mongo()
    db = await get_database()
    appinsights = await db[appinsights_collection_name].find({}).to_list(None)  # Modified
    return [AppInsightsInDB(**appinsights, id=str(appinsights["_id"])) for appinsights in appinsights]  # Modified


@app.post("/appinsights", response_model=AppInsightsInDB)  # Modified
async def create_appinsights(appinsights: AppInsights):  # Modified
    db = await get_database()
    appinsights_dict = appinsights.dict()
    result = await db[appinsights_collection_name].insert_one(appinsights_dict)  # Modified
    created_appinsights = await db[appinsights_collection_name].find_one({"_id": result.inserted_id})  # Modified

    if created_appinsights:
        return AppInsightsInDB(**created_appinsights, id=str(created_appinsights["_id"]))  # Modified
    else:
        raise HTTPException(status_code=500, detail="Failed to create AppInsights")  # Modified


@app.put("/appinsights/{appinsights_id}", response_model=AppInsightsInDB)  # Modified
async def update_appinsights(appinsights_id: str, appinsights: AppInsights):  # Modified
    db = await get_database()
    appinsights_dict = appinsights.dict()
    result = await db[appinsights_collection_name].update_one(
        {"_id": ObjectId(appinsights_id)},
        {"$set": appinsights_dict}
    )

    if result.modified_count == 1:
        updated_appinsights = await db[appinsights_collection_name].find_one(
            {"_id": ObjectId(appinsights_id)})  # Modified
        return AppInsightsInDB(**updated_appinsights, id=str(updated_appinsights["_id"]))  # Modified
    else:
        raise HTTPException(status_code=404, detail="AppInsights not found")  # Modified


@app.delete("/appinsights/{appinsights_id}", response_model=dict)  # Modified
async def delete_appinsights_by_id(appinsights_id: str):  # Modified
    db = await get_database()

    existing_appinsights = await db[appinsights_collection_name].find_one({"_id": ObjectId(appinsights_id)})  # Modified
    if existing_appinsights is None:
        raise HTTPException(status_code=404, detail="AppInsights not found")  # Modified

    result = await db[appinsights_collection_name].delete_one({"_id": ObjectId(appinsights_id)})  # Modified

    if result.deleted_count == 1:
        return {"message": f"AppInsights with ID '{appinsights_id}' deleted successfully"}  # Modified
    else:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the AppInsights")  # Modified


@app.get("/applications", response_model=List[ApplicationInDB])  # Modified
async def get_applications():  # Modified
    await connect_to_mongo()
    db = await get_database()
    applications = await db[application_collection_name].find({}).to_list(None)  # Modified
    return [ApplicationInDB(**application, id=str(application["_id"])) for application in applications]  # Modified


@app.post("/applications", response_model=ApplicationInDB)  # Modified
async def create_application(application: Application):  # Modified
    db = await get_database()
    application_dict = application.dict()
    result = await db[application_collection_name].insert_one(application_dict)  # Modified
    created_application = await db[application_collection_name].find_one({"_id": result.inserted_id})  # Modified

    if created_application:
        return ApplicationInDB(**created_application, id=str(created_application["_id"]))  # Modified
    else:
        raise HTTPException(status_code=500, detail="Failed to create Application")  # Modified


@app.put("/applications/{application_id}", response_model=ApplicationInDB)  # Modified
async def update_application(application_id: str, application: Application):  # Modified
    db = await get_database()
    application_dict = application.dict()
    result = await db[application_collection_name].update_one(
        {"_id": ObjectId(application_id)},
        {"$set": application_dict}
    )

    if result.modified_count == 1:
        updated_application = await db[application_collection_name].find_one(
            {"_id": ObjectId(application_id)})  # Modified
        return ApplicationInDB(**updated_application, id=str(updated_application["_id"]))  # Modified
    else:
        raise HTTPException(status_code=404, detail="Application not found")  # Modified


@app.delete("/applications/{application_id}", response_model=dict)  # Modified
async def delete_application_by_id(application_id: str):  # Modified
    db = await get_database()

    existing_application = await db[application_collection_name].find_one({"_id": ObjectId(application_id)})  # Modified
    if existing_application is None:
        raise HTTPException(status_code=404, detail="Application not found")  # Modified

    result = await db[application_collection_name].delete_one({"_id": ObjectId(application_id)})  # Modified

    if result.deleted_count == 1:
        return {"message": f"Application with ID '{application_id}' deleted successfully"}  # Modified
    else:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the Application")  # Modified


@app.get("/processes", response_model=List[ProcessInDB])  # Modified
async def get_processes():  # Modified
    await connect_to_mongo()
    db = await get_database()
    processes = await db[process_collection_name].find({}).to_list(None)  # Modified
    return [ProcessInDB(**process, id=str(process["_id"])) for process in processes]  # Modified


@app.post("/processes", response_model=ProcessInDB)  # Modified
async def create_process(process: Process):  # Modified
    db = await get_database()
    process_dict = process.dict()
    result = await db[process_collection_name].insert_one(process_dict)  # Modified
    created_process = await db[process_collection_name].find_one({"_id": result.inserted_id})  # Modified

    if created_process:
        return ProcessInDB(**created_process, id=str(created_process["_id"]))  # Modified
    else:
        raise HTTPException(status_code=500, detail="Failed to create Process")  # Modified


@app.put("/processes/{process_id}", response_model=ProcessInDB)  # Modified
async def update_process(process_id: str, process: Process):  # Modified
    db = await get_database()
    process_dict = process.dict()
    result = await db[process_collection_name].update_one(
        {"_id": ObjectId(process_id)},
        {"$set": process_dict}
    )

    if result.modified_count == 1:
        updated_process = await db[process_collection_name].find_one({"_id": ObjectId(process_id)})  # Modified
        return ProcessInDB(**updated_process, id=str(updated_process["_id"]))  # Modified
    else:
        raise HTTPException(status_code=404, detail="Process not found")  # Modified


@app.delete("/processes/{process_id}", response_model=dict)  # Modified
async def delete_process_by_id(process_id: str):  # Modified
    db = await get_database()

    existing_process = await db[process_collection_name].find_one({"_id": ObjectId(process_id)})  # Modified
    if existing_process is None:
        raise HTTPException(status_code=404, detail="Process not found")  # Modified

    result = await db[process_collection_name].delete_one({"_id": ObjectId(process_id)})  # Modified

    if result.deleted_count == 1:
        return {"message": f"Process with ID '{process_id}' deleted successfully"}  # Modified
    else:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the Process")  # Modified


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
