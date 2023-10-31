from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

MONGO_DB_URL = 'mongodb+srv://hr:hr@cluster0.aoqxdmb.mongodb.net/'
MONGO_DB_NAME = "FastAPI4"
employee_collection_name = "Employee"


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


class Employee(BaseModel):
    first_name: str
    last_name: str
    department: str
    salary: float


class EmployeeInDB(Employee):
    id: str


@app.get("/employees", response_model=List[EmployeeInDB])
async def get_employees():
    await connect_to_mongo()
    db = await get_database()
    employees = await db[employee_collection_name].find({}).to_list(None)
    return [EmployeeInDB(**employee, id=str(employee["_id"])) for employee in employees]


@app.post("/employees", response_model=EmployeeInDB)
async def create_employee(employee: Employee):
    db = await get_database()
    employee_dict = employee.dict()
    result = await db[employee_collection_name].insert_one(employee_dict)
    created_employee = await db[employee_collection_name].find_one({"_id": result.inserted_id})

    if created_employee:
        return EmployeeInDB(**created_employee, id=str(created_employee["_id"]))
    else:
        raise HTTPException(status_code=500, detail="Failed to create Employee")


@app.put("/employees/{employee_id}", response_model=EmployeeInDB)
async def update_employee(employee_id: str, employee: Employee):
    db = await get_database()
    employee_dict = employee.dict()
    result = await db[employee_collection_name].update_one(
        {"_id": ObjectId(employee_id)},
        {"$set": employee_dict}
    )

    if result.modified_count == 1:
        updated_employee = await db[employee_collection_name].find_one({"_id": ObjectId(employee_id)})
        return EmployeeInDB(**updated_employee, id=str(updated_employee["_id"]))
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


@app.delete("/employees/{employee_id}", response_model=dict)
async def delete_employee_by_id(employee_id: str):
    db = await get_database()

    existing_employee = await db[employee_collection_name].find_one({"_id": ObjectId(employee_id)})
    if existing_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    result = await db[employee_collection_name].delete_one({"_id": ObjectId(employee_id)})

    if result.deleted_count == 1:
        return {"message": f"Employee with ID '{employee_id}' deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the Employee")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
