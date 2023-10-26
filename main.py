from fastapi import FastAPI, File, UploadFile, HTTPException
import firebase_admin
from firebase_admin import credentials, storage
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {"storageBucket": "ayurveda-app-d0807.appspot.com"})
bucket = storage.bucket()
def upload_to_firebase(file: UploadFile) -> str:
    # Upload the image to Firebase Storage
    image_bytes = file.file.read()
    image_path = f"images/{file.filename}"
    blob = bucket.blob(image_path)
    blob.upload_from_string(image_bytes, content_type=file.content_type)

    # Get the public URL of the uploaded file
    image_url = blob.public_url

    return image_url

@app.post("/upload_image")
async def upload_image(
    file: UploadFile = File(...)
):
    # Upload the image and get the URL
    image_url = upload_to_firebase(file)

    return {"image_url": image_url}

# CORS middleware configuration
origins = [
    "http://192.168.8.100:8081",  # Replace this with your frontend's domain
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host='192.168.8.100', port=8000)
