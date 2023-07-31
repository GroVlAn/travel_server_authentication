from typing import Any, Optional, Dict

from pydantic import BaseModel


class MainResponse(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None
    details: Optional[Any] = None
