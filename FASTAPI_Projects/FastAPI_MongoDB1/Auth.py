from fastapi import FastAPI, HTTPException, status, Depends, Security, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

router = APIRouter(
    prefix='/Auth',
    tags=['Auth']

)
app = FastAPI()

# Define the HTTP Basic Authentication security
security = HTTPBasic()

# Mock username and password for demonstration purposes
correct_username = "stanleyjobson"
correct_password = "swordfish"


def authenticate_user(credentials: HTTPBasicCredentials = Security(security)):
    # Check if the provided credentials match the correct ones
    is_valid_username = secrets.compare_digest(credentials.username, correct_username)
    is_valid_password = secrets.compare_digest(credentials.password, correct_password)

    if not (is_valid_username and is_valid_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


@app.get("/users/me")
def read_current_user(username: str = Depends(authenticate_user)):
    return {"username": username}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
