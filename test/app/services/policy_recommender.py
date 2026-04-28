from typing import List
from schemas.schemas import UserProfileSchema, PolicySchema
from data.sample_policies import SAMPLE_POLICIES


def is_region_match(user_region: str | None, policy_region: str) -> bool:
    if policy_region == "전국":
        return True

    if user_region is None:
        return True

    return policy_region in user_region or user_region in policy_region


def is_age_match(age: int | None, policy: PolicySchema) -> bool:
    if age is None:
        return True

    return policy.age_min <= age <= policy.age_max


def is_category_match(profile: UserProfileSchema, policy: PolicySchema) -> bool:
    if not profile.policy_needs:
        return True

    return policy.category in profile.policy_needs


def recommend_policies(profile: UserProfileSchema) -> List[PolicySchema]:
    results = []

    for policy in SAMPLE_POLICIES:
        if not is_age_match(profile.age, policy):
            continue

        if not is_region_match(profile.region_text, policy.region):
            continue

        if not is_category_match(profile, policy):
            continue

        results.append(policy)

    return results