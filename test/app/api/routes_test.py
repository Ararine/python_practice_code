from fastapi import APIRouter
from app.schemas.request import PromptRequest
from app.schemas.user_profile import UserProfileSchema
from app.services.profile_builder import UserProfileBuilder

router = APIRouter()

profile_builder = UserProfileBuilder()


@router.post("/test/profile", response_model=UserProfileSchema)
def test_profile(request: PromptRequest):
    profile = profile_builder.build_profile(request.prompt)
    return profile