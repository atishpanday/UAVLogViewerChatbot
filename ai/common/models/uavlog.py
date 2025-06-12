from pydantic import BaseModel
from typing import Dict, Any, Union

class UAVLog(BaseModel):
    messageType: str
    messageList: Dict[str, list[Union[float, bool, str, None]]]
    dataType: Dict[str, Any]