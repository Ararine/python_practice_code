from fastapi import FastAPI
from typing import Optional, Literal, List
from pydantic import BaseModel
from google import genai
from google.genai import types


GEMINI_API_KEY = "api_key"
client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI()

PolicyInterest = Literal[
    "EMPLOYMENT",  # 취업
    "HOUSING",     # 주거
    "EDUCATION",   # 교육
    "WELFARE",     # 복지
    "FINANCE",     # 금융
]


class PromptRequest(BaseModel):
    text: str


class UserProfile(BaseModel):
    region: Optional[str] = None
    age: Optional[int] = None
    employment_condition: Optional[
        Literal[
            "ANY",
            "UNEMPLOYED",
            "JOB_SEEKER",
            "EMPLOYED",
            "PART_TIME",
            "STUDENT",
            "SELF_EMPLOYED",
            "FREELANCER",
            "STARTUP_PREP",
        ]
    ] = None
    housing_condition: Optional[
        Literal[
            "ANY",
            "HOMELESS",
            "OWNER",
            "RENT_MONTHLY",
            "RENT_JEONSE",
            "WITH_PARENTS",
            "SINGLE_HOUSEHOLD",
            "HEAD_OF_HOUSEHOLD",
            "LOCAL_RESIDENT",
        ]
    ] = None

    # 관심 정책 분야
    interest_fields: List[PolicyInterest] = []


@app.post("/extract-profile")
def extract_user_profile(req: PromptRequest):
    prompt = f"""
너는 청년정책 추천 시스템의 사용자 조건 추출기다.

사용자 문장에서 아래 정보를 JSON으로 추출해라.

[추출 규칙]
- 명시적으로 언급된 정보만 추출한다.
- 근거 없는 추론은 하지 않는다.
- 알 수 없는 값은 null 또는 빈 배열로 둔다.
- 나이는 숫자로 변환한다. 예: 스물다섯살 -> 25
- 관심 분야는 복수 선택 가능하다.

[관심 분야 코드]
- 취업, 구직, 일자리, 채용, 인턴, 창업 준비 → EMPLOYMENT
- 주거, 월세, 전세, 집, 임대, 보증금 → HOUSING
- 교육, 강의, 수업, 학원, 자격증, 훈련 → EDUCATION
- 복지, 생활지원, 건강, 돌봄, 문화, 심리상담 → WELFARE
- 금융, 대출, 자금, 저축, 적금, 이자, 신용 → FINANCE

사용자 문장:
{req.text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=UserProfile,
            temperature=0,
        ),
    )

    return response.parsed