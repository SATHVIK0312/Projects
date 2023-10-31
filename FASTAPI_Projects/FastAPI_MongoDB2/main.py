from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

MONGO_DB_URL = 'mongodb+srv://hr:hr@cluster0.aoqxdmb.mongodb.net/'
MONGO_DB_NAME = "FastAPI2"
campus_collection_name = "Campus"
department_collection_name = "Department"
student_collection_name = "Students"


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


class Campus(BaseModel):
    campus_id: str
    name: str
    city: str


class CampusInDB(Campus):
    id: str


class Department(BaseModel):
    department_id: str
    department_name: str
    seats: int
    HOD_id: str


class DepartmentInDB(Department):
    id: str


class Student(BaseModel):
    student_id: str
    student_name: str
    PhoneNo: str
    emailid: str
    department_id: str


class StudentInDB(Student):
    id: str


@app.get("/campus", response_model=List[CampusInDB])
async def get_campuses():
    await connect_to_mongo()
    db = await get_database()
    campuses = await db[campus_collection_name].find({}).to_list(None)
    return [CampusInDB(**campus, id=str(campus["_id"])) for campus in campuses]


@app.post("/campus", response_model=CampusInDB)
async def create_campus(campus: Campus):
    db = await get_database()
    campus_dict = campus.dict()
    result = await db[campus_collection_name].insert_one(campus_dict)
    created_campus = await db[campus_collection_name].find_one({"_id": result.inserted_id})

    if created_campus:
        return CampusInDB(**created_campus, id=str(created_campus["_id"]))
    else:
        raise HTTPException(status_code=500, detail="Failed to create campus")


@app.put("/campus/{campus_id}", response_model=CampusInDB)
async def update_campus(campus_id: str, campus: Campus):
    db = await get_database()
    campus_dict = campus.dict()
    result = await db[campus_collection_name].update_one(
        {"_id": ObjectId(campus_id)},
        {"$set": campus_dict}
    )

    if result.modified_count == 1:
        updated_campus = await db[campus_collection_name].find_one({"_id": ObjectId(campus_id)})
        return CampusInDB(**updated_campus, id=str(updated_campus["_id"]))
    else:
        raise HTTPException(status_code=404, detail="Campus not found")


@app.delete("/campus/{campus_id}", response_model=dict)
async def delete_campus_by_id(campus_id: str):
    db = await get_database()

    existing_campus = await db[campus_collection_name].find_one({"_id": ObjectId(campus_id)})
    if existing_campus is None:
        raise HTTPException(status_code=404, detail="Campus not found")

    result = await db[campus_collection_name].delete_one({"_id": ObjectId(campus_id)})

    if result.deleted_count == 1:
        return {"message": f"Campus with ID '{campus_id}' deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the campus")


@app.get("/department", response_model=List[DepartmentInDB])
async def get_departments():  # Modified
    await connect_to_mongo()
    db = await get_database()
    departments = await db[department_collection_name].find({}).to_list(None)
    return [DepartmentInDB(**department, id=str(department["_id"])) for department in departments]


@app.post("/department", response_model=DepartmentInDB)
async def create_department(department: Department):
    db = await get_database()
    department_dict = department.dict()
    result = await db[department_collection_name].insert_one(department_dict)
    created_department = await db[department_collection_name].find_one({"_id": result.inserted_id})

    if created_department:
        return DepartmentInDB(**created_department, id=str(created_department["_id"]))
    else:
        raise HTTPException(status_code=500, detail="Failed to create department")


@app.put("/department/{department_id}", response_model=DepartmentInDB)
async def update_department(department_id: str, department: Department):
    db = await get_database()
    department_dict = department.dict()
    result = await db[department_collection_name].update_one(
        {"_id": ObjectId(department_id)},
        {"$set": department_dict}
    )

    if result.modified_count == 1:
        updated_department = await db[department_collection_name].find_one({"_id": ObjectId(department_id)})
        return DepartmentInDB(**updated_department, id=str(updated_department["_id"]))
    else:
        raise HTTPException(status_code=404, detail="Department not found")


@app.delete("/department/{department_id}", response_model=dict)
async def delete_department_by_id(department_id: str):
    db = await get_database()

    existing_department = await db[department_collection_name].find_one({"_id": ObjectId(department_id)})
    if existing_department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    result = await db[department_collection_name].delete_one({"_id": ObjectId(department_id)})

    if result.deleted_count == 1:
        return {"message": f"Department with ID '{department_id}' deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the department")



@app.get("/student", response_model=List[StudentInDB])
async def get_students():
    await connect_to_mongo()
    db = await get_database()
    students = await db[student_collection_name].find({}).to_list(None)
    return [StudentInDB(**student, id=str(student["_id"])) for student in students]


@app.post("/student", response_model=StudentInDB)
async def create_student(student: Student):
    db = await get_database()
    student_dict = student.dict()
    result = await db[student_collection_name].insert_one(student_dict)
    created_student = await db[student_collection_name].find_one({"_id": result.inserted_id})

    if created_student:
        return StudentInDB(**created_student, id=str(created_student["_id"]))
    else:
        raise HTTPException(status_code=500, detail="Failed to create student")


@app.put("/student/{student_id}", response_model=StudentInDB)
async def update_student(student_id: str, student: Student):
    student_dict = student.dict()
    result = await db[student_collection_name].update_one(
        {"_id": ObjectId(student_id)},
        {"$set": student_dict}
    )

    if result.modified_count == 1:
        updated_student = await db[student_collection_name].find_one({"_id": ObjectId(student_id)})
        return StudentInDB(**updated_student, id=str(updated_student["_id"]))
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@app.delete("/student/{student_id}", response_model=dict)
async def delete_student_by_id(student_id: str):
    db = await get_database()

    existing_student = await db[student_collection_name].find_one({"_id": ObjectId(student_id)})
    if existing_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    result = await db[student_collection_name].delete_one({"_id": ObjectId(student_id)})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
