from pydantic import BaseModel
from typing import Dict, Any, Union, Optional

class UAVLog(BaseModel):
    messageType: str
    messageList: Dict[str, list[Union[float, bool, str, None]]]
    messageListStats: Optional[Dict[str, Dict[str, Any]]] = {}
    dataType: Dict[str, Any]