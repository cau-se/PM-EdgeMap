from pydantic import BaseModel
from src.algorithm.data_structures.conformance_score import SConformanceScore

class SConformanceValues(BaseModel):
    case_id: str
    last_activity: str | None
    conformance: SConformanceScore
