from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/health", status_code=200)
async def health():
    try:
        return {'result': 'OK'}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))