from pydantic import BaseModel

class SConformanceScore(BaseModel):
    path_length: int
    conformance_violations: int
