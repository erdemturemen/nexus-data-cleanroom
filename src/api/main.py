"""
NEXUS Data Cleanroom API - CORS düzeltildi
"""
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import pandas as pd

app = FastAPI(title="NEXUS Data Cleanroom API")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "NEXUS Data Cleanroom API",
        "status": "çalışıyor",
        "version": "1.0"
    }

@app.get("/health")
def health():
    return {"status": "sağlıklı"}

@app.post("/api/upload")
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        import io
        df = pd.read_csv(io.BytesIO(contents))
        
        return {
            "success": True,
            "message": "CSV yüklendi!",
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist()
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Hata: {str(e)}"
        }

if __name__ == "__main__":
    print("🚀 NEXUS API başlatılıyor...")
    print("📍 URL: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
