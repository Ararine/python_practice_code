from schemas.schemas import PolicySchema


SAMPLE_POLICIES = [
    PolicySchema(
        policy_id=1,
        policy_name="청년 월세 지원",
        region="서울",
        age_min=19,
        age_max=39,
        category="housing",
        description="청년의 월세 부담 완화를 위한 주거비 지원 정책입니다.",
        apply_url="https://example.com/housing"
    ),
    PolicySchema(
        policy_id=2,
        policy_name="청년 취업 지원 프로그램",
        region="전국",
        age_min=18,
        age_max=34,
        category="job",
        description="취업 준비 청년을 위한 상담, 교육, 면접 지원 프로그램입니다.",
        apply_url="https://example.com/job"
    ),
    PolicySchema(
        policy_id=3,
        policy_name="청년 생활비 대출",
        region="전국",
        age_min=19,
        age_max=39,
        category="loan",
        description="청년층의 생활 안정을 위한 저금리 생활비 대출 정책입니다.",
        apply_url="https://example.com/loan"
    ),
    PolicySchema(
        policy_id=4,
        policy_name="국민취업지원제도",
        region="전국",
        age_min=15,
        age_max=69,
        category="job",
        description="구직자에게 취업지원서비스와 수당을 제공하는 제도입니다.",
        apply_url="https://example.com/employment"
    ),
]