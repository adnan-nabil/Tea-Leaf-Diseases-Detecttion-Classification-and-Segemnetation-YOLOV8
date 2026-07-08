import os
import httpx
import base64
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Tea Leaf Disease Detector Gateway",
    description="Gateway API that routes image uploads to a hosted Hugging Face YOLOv8 space."
)

# 1. Mount the static directory for the Frontend UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Backend gateway is running, but index.html was not found."}

# 2. Define Hugging Face Space Target Endpoint
HF_API_URL = "https://n25-bd-yolov8-tea.hf.space/predict"

# 3. Gateway Inference Endpoint
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    try:
        file_bytes = await file.read()
        files = {"file": (file.filename, file_bytes, file.content_type)}

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(HF_API_URL, files=files)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"Hugging Face Space API error (Status {response.status_code})"
                )
            
            # Check the content type returned by your HF Space
            content_type = response.headers.get("content-type", "")
            
            # CASE 1: The HF space returns a raw image file directly
            if "image" in content_type or response.content.startswith(b'\xff\xd8'):
                # Convert the raw image bytes into a base64 string for the UI
                img_base64 = base64.b64encode(response.content).decode('utf-8')
                return JSONResponse(content={
                    "success": True,
                    "predictions": [], # Space returned just the image, no text stats
                    "image": f"data:image/jpeg;base64,{img_base64}"
                })
            
            # CASE 2: The HF space returns a standard JSON object
            else:
                hf_data = response.json()
                return JSONResponse(content=hf_data)

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503, 
            detail=f"Could not reach Hugging Face inference server: {str(exc)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal gateway error: {str(e)}")