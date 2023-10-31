from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from hello import app as hello_app

app = FastAPI()

MONGO_DB_URL = 'mongodb+srv://hr:hr@cluster0.aoqxdmb.mongodb.net/'
MONGO_DB_NAME = "FastAPI"
department_collection_name = "Departments"
section_collection_name = "Sections"
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


class Department(BaseModel):
    departmentName: str


class DepartmentInDB(Department):
    id: str


class Section(BaseModel):
    departmentName: str
    section: str


class SectionInDB(Section):
    id: str


class Student(BaseModel):
    student_name: str
    section: str
    departmentName: str


class StudentInDB(Student):
    id: str


@app.get("/departments", response_model=List[DepartmentInDB])
async def get_departments():
    await connect_to_mongo()
    db = await get_database()
    departments = await db[department_collection_name].find({}).to_list(None)
    return [DepartmentInDB(**department, id=str(department["_id"])) for department in departments]


@app.post("/departments", response_model=DepartmentInDB)
async def create_department(department: Department):
    db = await get_database()
    department_dict = department.dict()
    result = await db[department_collection_name].insert_one(department_dict)
    created_department = await db[department_collection_name].find_one({"_id": result.inserted_id})

    if created_department:
        return DepartmentInDB(**created_department, id=str(created_department["_id"]))
    else:
        raise HTTPException(status_code=500, detail="Failed to create department")


@app.put("/departments/{department_id}", response_model=DepartmentInDB)
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


@app.delete("/departments/{department_id}", response_model=dict)
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


@app.get("/sections", response_model=List[SectionInDB])
async def get_sections():
    await connect_to_mongo()
    db = await get_database()
    sections = await db[section_collection_name].find({}).to_list(None)
    return [SectionInDB(**section, id=str(section["_id"])) for section in sections]


@app.post("/sections", response_model=SectionInDB)
async def create_section(section: Section):
    db = await get_database()
    section_dict = section.dict()
    result = await db[section_collection_name].insert_one(section_dict)
    created_section = await db[section_collection_name].find_one({"_id": result.inserted_id})

    if created_section:
        return SectionInDB(**created_section, id=str(created_section["_id"]))
    else:
        raise HTTPException(status_code=500, detail="Failed to create section")


@app.put("/sections/{section_id}", response_model=SectionInDB)
async def update_section(section_id: str, section: Section):
    db = await get_database()
    section_dict = section.dict()
    result = await db[section_collection_name].update_one(
        {"_id": ObjectId(section_id)},
        {"$set": section_dict}
    )

    if result.modified_count == 1:
        updated_section = await db[section_collection_name].find_one({"_id": ObjectId(section_id)})
        return SectionInDB(**updated_section, id=str(updated_section["_id"]))
    else:
        raise HTTPException(status_code=404, detail="Section not found")


@app.delete("/sections/{section_id}", response_model=dict)
async def delete_section_by_id(section_id: str):
    db = await get_database()

    existing_section = await db[section_collection_name].find_one({"_id": ObjectId(section_id)})
    if existing_section is None:
        raise HTTPException(status_code=404, detail="Section not found")

    result = await db[section_collection_name].delete_one({"_id": ObjectId(section_id)})

    if result.deleted_count == 1:
        return {"message": f"Section with ID '{section_id}' deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the section")


@app.get("/students", response_model=List[StudentInDB])
async def get_students():
    await connect_to_mongo()
    db = await get_database()
    students = await db[student_collection_name].find({}).to_list(None)
    return [StudentInDB(**student, id=str(student["_id"])) for student in students]


@app.post("/students", response_model=StudentInDB)
async def create_student(student: Student):
    db = await get_database()
    student_dict = student.dict()
    result = await db[student_collection_name].insert_one(student_dict)
    created_student = await db[student_collection_name].find_one({"_id": result.inserted_id})

    if created_student:
        return StudentInDB(**created_student, id=str(created_student["_id"]))
    else:
        raise HTTPException(status_code=500, detail="Failed to create student")


@app.put("/students/{student_id}", response_model=StudentInDB)
async def update_student(student_id: str, student: Student):
    db = await get_database()
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


@app.delete("/students/{student_id}", response_model=dict)
async def delete_student_by_id(student_id: str):
    db = await get_database()

    existing_student = await db[student_collection_name].find_one({"_id": ObjectId(student_id)})
    if existing_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    result = await db[student_collection_name].delete_one({"_id": ObjectId(student_id)})

    if result.deleted_count == 1:
        return {"message": f"Student with ID '{student_id}' deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the student")


app.mount("/hello", hello_app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
