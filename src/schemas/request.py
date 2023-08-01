from typing import Any, Optional, Dict, List

from pydantic import BaseModel


class MainResponse(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None
    details: Optional[Any] = None


class ExceptionDetails(BaseModel):
    field: str
    errors: List[str]


class ExceptionResponse(BaseModel):
    status: str
    details: ExceptionDetails
