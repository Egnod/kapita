from __future__ import annotations

import datetime

from pydantic import BaseModel, Field


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime.datetime) -> str:
    return dt.isoformat() if dt.tzinfo else dt.replace(tzinfo=datetime.UTC).isoformat()


class BaseDTO(BaseModel):
    """BaseDTO"""

    class Config:
        """Config."""

        from_attributes = True
        json_encoders = {datetime.datetime: convert_datetime_to_iso_8601_with_z_suffix}


class StatusStub(BaseModel):
    """StatusStub"""

    status: bool = Field(default=True)
    details: str | None = Field(default=None)


class UserTokenDTO(BaseDTO):
    token: str
