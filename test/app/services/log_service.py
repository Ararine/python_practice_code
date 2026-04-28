import json
from datetime import datetime
from schemas.schemas import UserProfileSchema


LOG_FILE_PATH = "user_prompt_logs.jsonl"


def save_user_prompt_log(profile: UserProfileSchema) -> None:
    log_data = {
        "created_at": datetime.now().isoformat(),
        "raw_text": profile.raw_text,
        "age": profile.age,
        "region_text": profile.region_text,
        "employment_status": profile.employment_status,
        "education_status": profile.education_status,
        "housing_status": profile.housing_status,
        "income_status": profile.income_status,
        "policy_needs": profile.policy_needs,
        "used_zero_shot": profile.used_zero_shot,
        "confidence": profile.confidence,
    }

    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + "\n")