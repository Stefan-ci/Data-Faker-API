from uuid import UUID
from pydantic import Field
from datetime import datetime
from utils.base import CustomBaseModel, CustomPaginationBaseModel

class AttendanceModel(CustomBaseModel):
    employee_id: UUID
    check_in: datetime
    check_out: datetime
    worked_hours: float


class AttendancePaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated Attendance list """
    results: list[AttendanceModel] = Field(default_factory=list)
