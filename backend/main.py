from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from gemini_analyzer import GeminiMRIAnalyzer
from PIL import Image
import io
import base64

app = FastAPI(title="MRI Analysis XAI API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini analyzer
analyzer = GeminiMRIAnalyzer()

@app.get("/")
async def root():
    return {"message": "MRI Analysis XAI API - Upload MRI images to /analyze endpoint"}

@app.post("/analyze")
async def analyze_mri(file: UploadFile = File(...)):
    """
    Analyze uploaded MRI image using Gemini API
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Analyze with Gemini
        result = analyzer.analyze_mri(image)
        
        # Convert image to base64 for response
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return JSONResponse(content={
            "success": True,
            "image_base64": img_str,
            "analysis": result
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Check if API and Gemini connection are working"""
    try:
        api_key_set = bool(os.getenv("GEMINI_API_KEY"))
        return {
            "status": "healthy",
            "gemini_api_configured": api_key_set
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
