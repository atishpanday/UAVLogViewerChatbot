from fastapi import APIRouter, HTTPException
from .schema import UAVLogRequest
from data.save_data import save_data

router = APIRouter(prefix="/uavlogs")


@router.post("", status_code=201)
async def uavlogs(request: UAVLogRequest):
    try:
        ids = await save_data(request.logs)
        str_ids = [str(id) for id in ids]
        return {"message": "Data saved successfully", "ids": str_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))