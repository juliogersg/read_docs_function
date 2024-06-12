from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
import os
import tempfile
from api.utils.orchestator import Orchestator

router = APIRouter()
orchestator = Orchestator()

@router.post("/salary", status_code=200)
async def salary(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        # Generate temp file name
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, file.filename)

        # Read excel and save it in temp file
        contents = await file.read()
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(contents)

        # Process 
        result = orchestator.process_salary(temp_file_path)

        # Delete temp files
        background_tasks.add_task(orchestator.delete_file, temp_file_path)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/payments", status_code=200)
async def payments(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        # Generate temp file name
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, file.filename)

        # Read excel and save it in temp file
        contents = await file.read()
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(contents)

        # Process 
        result = orchestator.process_payments(temp_file_path)

        # Delete temp files
        background_tasks.add_task(orchestator.delete_file, temp_file_path)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/salary-vision", status_code=200)
async def salary(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        # Generate temp file name
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, file.filename)

        # Read excel and save it in temp file
        contents = await file.read()
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(contents)

        # Process 
        result = orchestator.process_salary_vision(temp_file_path)

        # Delete temp files
        background_tasks.add_task(orchestator.delete_file, temp_file_path)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
