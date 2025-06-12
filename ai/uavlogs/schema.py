from pydantic import BaseModel
from common.models.uavlog import UAVLog

class UAVLogRequest(BaseModel):
    logs: list[UAVLog]