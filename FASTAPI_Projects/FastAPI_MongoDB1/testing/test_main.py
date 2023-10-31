import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_departments():
    response = client.get("/departments")
    assert response.status_code == 200
    assert response.json() == [
        {
            "departmentName": "CSE",
            "id": "650189af9761dbc01d903b8f"
        },
        {
            "departmentName": "ECE",
            "id": "65018b1e9761dbc01d903b93"
        },
        {
            "departmentName": "IT",
            "id": "65018b309761dbc01d903b94"
        },
        {
            "departmentName": "CSE - DS",
            "id": "65029d265f86c2c2f830cafc"
        },
        {
            "departmentName": "CSE - AI/ML",
            "id": "65029d385f86c2c2f830cafd"
        },
        {
            "departmentName": "Civil",
            "id": "6502a35f6851085bdb62bf01"
        }
    ]


def test_get_sections():
    response = client.get("/sections")
    assert response.status_code == 200
    assert response.json() == [
  {
    "departmentName": "CSE",
    "section": "A1",
    "id": "6502d5468f00e54c7564efd0"
  },
  {
    "departmentName": "CSE",
    "section": "A2",
    "id": "6502d5538f00e54c7564efd1"
  },
  {
    "departmentName": "ECE",
    "section": "A2",
    "id": "6502d5588f00e54c7564efd2"
  },
  {
    "departmentName": "ECE",
    "section": "A1",
    "id": "6502d55d8f00e54c7564efd3"
  },
  {
    "departmentName": "CSE",
    "section": "B1",
    "id": "6502d5688f00e54c7564efd4"
  },
  {
    "departmentName": "CSE",
    "section": "B2",
    "id": "6502d56b8f00e54c7564efd5"
  },
  {
    "departmentName": "CSE - DS",
    "section": "A1",
    "id": "6502d57b8f00e54c7564efd6"
  },
  {
    "departmentName": "CSE - AI/ML",
    "section": "A1",
    "id": "6502d5868f00e54c7564efd7"
  },
  {
    "departmentName": "IT",
    "section": "A1",
    "id": "6502d58e8f00e54c7564efd8"
  },
  {
    "departmentName": "IT",
    "section": "A2",
    "id": "6502d5938f00e54c7564efd9"
  }
]


def test_get_students():
    response = client.get("/students")
    assert response.status_code == 200
    assert response.json() == [
  {
    "student_name": "Sathvik",
    "section": "A1",
    "departmentName": "CSE - DS",
    "id": "6502d86c84c539497ccb16d4"
  },
  {
    "student_name": "Chetan",
    "section": "A1",
    "departmentName": "CSE - AI/ML",
    "id": "6502d8be84c539497ccb16d5"
  },
  {
    "student_name": "Pawan",
    "section": "B1",
    "departmentName": "CSE",
    "id": "6502d8d584c539497ccb16d6"
  },
  {
    "student_name": "Mahin",
    "section": "A1",
    "departmentName": "IT",
    "id": "6502d8ef84c539497ccb16d7"
  }
]



