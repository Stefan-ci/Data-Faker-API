from pydantic import Field
from datetime import datetime
from utils.base import CustomBaseModel, CustomPaginationBaseModel

class AnalyticModel(CustomBaseModel):
    metric_name: str
    value: float
    trend: float = Field(..., description="Variations in percentage")
    category: str = Field(..., description="KPI category")
    unit: str = Field(..., description="Unit of measurement (%, $, visits...)")
    previous_value: float = Field(..., description="Previous value for comparison")
    timestamp: datetime


class AnalyticPaginationResponse(CustomPaginationBaseModel):
    """ Response model for paginated analytics list """
    results: list[AnalyticModel] = Field(default_factory=list)
