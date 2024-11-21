from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import List, Optional
import base64
import mimetypes
import os

app = FastAPI()

# Helper function to check for primes
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

class RequestData(BaseModel):
    data: List[str]
    file_b64: Optional[str] = None

@app.post("/bfhl")
async def process_data(payload: RequestData):
    try:
        data = payload.data
        file_b64 = payload.file_b64

        numbers = [x for x in data if x.isdigit()]
        alphabets = [x for x in data if x.isalpha()]
        highest_lower = [max([x for x in data if x.islower()], default="")]

        # File validation
        file_valid = False
        mime_type = None
        file_size = None
        if file_b64:
            try:
                file_bytes = base64.b64decode(file_b64)
                mime_type = mimetypes.guess_type("temp_file")[0]
                file_size = len(file_bytes) / 1024
                file_valid = True
            except Exception:
                file_valid = False

        return {
            "is_success": True,
            "user_id": "your_name_ddmmyyyy",
            "email": "your_college_email",
            "roll_number": "your_roll_number",
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_lowercase_alphabet": highest_lower,
            "is_prime_found": any(is_prime(int(n)) for n in numbers),
            "file_valid": file_valid,
            "file_mime_type": mime_type,
            "file_size_kb": file_size,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/bfhl")
async def get_operation_code():
    return {"operation_code": 1}
