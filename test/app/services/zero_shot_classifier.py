from typing import Tuple, Optional, List
from transformers import pipeline
from schemas.schemas import UserProfileSchema


classifier = pipeline(
    "zero-shot-classification",
    model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
)


EMPLOYMENT_LABELS = {
    "job_seeker": "취업을 준비하거나 구직 중인 상태",
    "unemployed": "현재 직업이 없고 소득이 없는 상태",
    "employed": "회사에 다니거나 근로 중인 상태",
    "self_employed": "프리랜서 또는 개인사업자 상태",
}

EDUCATION_LABELS = {
    "student": "학교에 재학 중인 학생 상태",
    "leave_of_absence": "학교를 휴학 중인 상태",
    "graduate": "학교를 졸업한 상태",
}

HOUSING_LABELS = {
    "monthly_rent": "월세 또는 집세 부담이 있는 상태",
    "jeonse": "전세 보증금 관련 지원이 필요한 상태",
    "living_alone": "혼자 살거나 자취 중인 상태",
    "with_parents": "부모님 또는 가족과 함께 사는 상태",
}

POLICY_NEED_LABELS = {
    "housing": "주거 지원, 월세 지원, 전세 지원이 필요한 상황",
    "job": "취업 지원, 구직 지원, 일자리 지원이 필요한 상황",
    "education": "교육, 직업훈련, 강의 수강 지원이 필요한 상황",
    "loan": "대출, 융자, 생활비 대출이 필요한 상황",
    "income": "현금성 지원금, 수당, 생활비 지원이 필요한 상황",
    "startup": "창업이나 사업 지원이 필요한 상황",
}


def classify_zero_shot(
    text: str,
    label_map: dict[str, str],
    threshold: float = 0.55
) -> Tuple[Optional[str], Optional[float]]:
    candidate_labels = list(label_map.values())

    result = classifier(
        text,
        candidate_labels=candidate_labels,
        hypothesis_template="이 문장은 {}를 의미한다."
    )

    best_label_text = result["labels"][0]
    best_score = float(result["scores"][0])

    if best_score < threshold:
        return None, best_score

    for key, value in label_map.items():
        if value == best_label_text:
            return key, best_score

    return None, best_score


def classify_zero_shot_multi(
    text: str,
    label_map: dict[str, str],
    threshold: float = 0.55
) -> List[str]:
    result = classifier(
        text,
        candidate_labels=list(label_map.values()),
        hypothesis_template="이 문장은 {}를 의미한다.",
        multi_label=True
    )

    selected = []

    for label_text, score in zip(result["labels"], result["scores"]):
        if float(score) >= threshold:
            for key, value in label_map.items():
                if value == label_text:
                    selected.append(key)

    return selected


def enrich_with_zero_shot(profile: UserProfileSchema) -> UserProfileSchema:
    text = profile.raw_text
    scores = []

    if profile.employment_status is None:
        label, score = classify_zero_shot(text, EMPLOYMENT_LABELS)
        profile.employment_status = label
        if score is not None:
            scores.append(score)

    if profile.education_status is None:
        label, score = classify_zero_shot(text, EDUCATION_LABELS)
        profile.education_status = label
        if score is not None:
            scores.append(score)

    if profile.housing_status is None:
        label, score = classify_zero_shot(text, HOUSING_LABELS)
        profile.housing_status = label
        if score is not None:
            scores.append(score)

    if not profile.policy_needs:
        profile.policy_needs = classify_zero_shot_multi(text, POLICY_NEED_LABELS)

    profile.used_zero_shot = True

    if scores:
        profile.confidence = sum(scores) / len(scores)

    return profile