from typing import Optional, List
from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    prompt: str


class UserProfileSchema(BaseModel):
    raw_text: str

    age: Optional[int] = None
    region_text: Optional[str] = None

    employment_status: Optional[str] = None
    education_status: Optional[str] = None
    housing_status: Optional[str] = None
    income_status: Optional[str] = None

    policy_needs: List[str] = Field(default_factory=list)

    used_zero_shot: bool = False
    confidence: Optional[float] = None


class PolicySchema(BaseModel):
    policy_id: int
    policy_name: str
    region: str
    age_min: int
    age_max: int
    category: str
    description: str
    apply_url: Optional[str] = None


class RecommendResponse(BaseModel):
    profile: UserProfileSchema
    policies: List[PolicySchema]