import uvicorn
import logging
from fastapi import FastAPI
from schemas.schemas import PromptRequest, RecommendResponse
from services.rule_extractor import extract_by_rules
from services.zero_shot_classifier import enrich_with_zero_shot
from services.policy_recommender import recommend_policies
from services.log_service import save_user_prompt_log

app = FastAPI()

def needs_model_help(profile) -> bool:
    """
    룰 기반으로 충분하지 않은 경우 zero-shot 모델 사용
    """
    if profile.employment_status is None:
        return True

    if profile.education_status is None:
        return True

    if profile.housing_status is None and not profile.policy_needs:
        return True

    if not profile.policy_needs:
        return True

    return False


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(request: PromptRequest):
    # 1. 룰 기반 추출
    print(f"##### request.prompt : {request.prompt} #####")
    profile = extract_by_rules(request.prompt)
    
    print(f"##### profile : {profile} #####")

    # 2. 부족한 값이 있으면 Zero-shot 모델 보조
    if needs_model_help(profile):
        profile = enrich_with_zero_shot(profile)
        
    print(f"##### profile : {profile} #####")

    # 3. 사용자 로그 저장
    save_user_prompt_log(profile)

    # 4. 정책 추천
    policies = recommend_policies(profile)
    
    print(f"##### policies : {policies} #####")

    return RecommendResponse(
        profile=profile,
        policies=policies
    )
    
# uvicorn.run(app, host="0.0.0.0", port="8000", reload=True)