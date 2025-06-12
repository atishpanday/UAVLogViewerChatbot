from fastapi import APIRouter
from .schema import UAVLogRequest
from data.save_data import save_data

router = APIRouter(prefix="/uavlogs")


@router.post("")
async def uavlogs(request: UAVLogRequest):
    ids = await save_data(request.logs)
    str_ids = [str(id) for id in ids]
    return {"message": "Data saved successfully", "ids": str_ids}