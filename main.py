from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
from cryptography.fernet import Fernet

# Generate a key for encryption and decryption
# In a real application, you should store this key securely
key = Fernet.generate_key()
cipher_suite = Fernet(key)

app = FastAPI()

BASE_URL = "https://reqres.in"


class LoginRequest(BaseModel):
    email: str
    password: str


# define auth logged in from reqres.in
@app.post("/auth")
async def login(request: LoginRequest):
    payload = request.model_dump()
    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL + "/api/login", json=payload)        
        if response.status_code == 200:
            # Encrypt the password
            encrypted_password = cipher_suite.encrypt(request.password.encode())

            data = {
                "email": request.email,
                "password": encrypted_password.decode(),
                "token": response.json()["token"],
            }
            return {
                "data": data,
                "status_code": response.status_code,
                "message": "Login successful",
                "success": True,
            }
 
        elif response.status_code == 400 and "error" in response.json():
            error_message = response.json()["error"]
            if error_message == "user not found":
                return {
                    "data": {},
                    "status_code": response.status_code,
                    "message": "User not found" if error_message == "user not found" else error_message,
                    "success": False,
                }
            
        elif request.email != "" and "error" in response.json():
            error_message = response.json()["error"]
            if error_message == "Missing email or username":
                return {
                    "data": {},
                    "status_code": response.status_code,
                    "message": "Email is required" if error_message == "Missing email or username" else error_message,
                    "success": False,
                }
                
        elif request.password == "" and "error" in response.json():
            error_message = response.json()["error"]
            if error_message == "Missing password":
                return {
                    "data": {},
                    "status_code": response.status_code,
                    "message": "Password is required" if error_message == "Missing password" else error_message,
                    "success": False,
                }
                
        else:
            return {
                "data": {},
                "status_code": response.status_code,
                "message": response.json()["error"],
                "success": False,
            }


# define get user from reqres.in
@app.get("/get-users")
async def get_users(page: int = Query(1, description="Page number to fetch")):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/users?page={page}")

        try:
            if response.status_code == 200:
                data = response.json()
                return {
                    "paging": {
                        "page": data["page"],
                        "per_page": data["per_page"],
                        "total": data["total"],
                        "total_pages": data["total_pages"]
                    },
                    "data": data["data"],
                    "status_code": response.status_code,
                    "message": "All Users found",
                    "success": True,
                }
            else:
                return {
                    "data": {},
                    "status_code": response.status_code,
                    "message": response.json()["error"],
                    "success": False,
                }

        except:
            return {
                "data": {},
                "status_code": response.status_code,
                "message": response.json()["error"],
                "success": False,
            }


@app.get("/get-user/{user_id}")
async def get_user(user_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://reqres.in/api/users/{user_id}")

        data = response.json()

        if not user_id.isdigit():
            return {
                "data": {},
                "status_code": 422,
                "message": "Unprocessable Entity : Special Character not Allowed",
                "success": False,
            }

        if response.status_code == 404:
            return {
                "data": {},
                "status_code": 404,
                "message": "Data not Found",
                "success": False,
            }

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Unexpected error occurred")

        # Check if the user data is available
        if "data" in data and data["data"]:
            return {
                "data": data["data"],
                "status_code": 200,
                "message": "Data found",
                "success": True,
            }

        # Fallback for unexpected cases
        return {
            "data": {},
            "status_code": response.status_code,
            "message": "Data not found",
            "success": False,
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
