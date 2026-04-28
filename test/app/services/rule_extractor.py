import re
from typing import Optional, List
from schemas.schemas import UserProfileSchema


EMPLOYMENT_KEYWORDS = {
    "job_seeker": ["취준", "취준생", "취업준비", "구직중", "구직"],
    "unemployed": ["무직", "백수", "실업", "일 안함", "일안함"],
    "employed": ["직장인", "재직", "근무중", "회사원", "알바", "아르바이트"],
    "self_employed": ["자영업", "개인사업자", "프리랜서"],
}

EDUCATION_KEYWORDS = {
    "student": ["대학생", "학생", "재학생"],
    "leave_of_absence": ["휴학생", "휴학", "학교 쉬고"],
    "graduate": ["졸업생", "졸업"],
}

HOUSING_KEYWORDS = {
    "monthly_rent": ["월세", "반전세"],
    "jeonse": ["전세"],
    "living_alone": ["자취", "혼자 살아", "1인가구", "일인가구"],
    "with_parents": ["부모님이랑", "본가", "가족이랑"],
}

INCOME_KEYWORDS = {
    "low_income": ["저소득", "기초생활수급", "차상위", "중위소득"],
    "no_income": ["소득 없음", "수입 없음", "무소득", "돈 못 벌"],
}

POLICY_NEED_KEYWORDS = {
    "housing": ["월세", "전세", "주거", "임대", "보증금", "자취"],
    "job": ["취업", "구직", "면접", "자소서", "일자리"],
    "education": ["교육", "훈련", "강의", "수강", "국비"],
    "loan": ["대출", "융자", "생활비"],
    "income": ["지원금", "수당", "현금", "생활지원"],
    "startup": ["창업", "사업", "스타트업"],
}

REGION_PATTERN = re.compile(
    r"([가-힣A-Za-z0-9]+(?:특별시|광역시|도|시|군|구|동|읍|면|리|로|길|사거리|역))"
)

INVALID_REGION_WORDS = {
    "어디로",
    "여기로",
    "저기로",
    "거기로",
    "이리로",
    "저리로",
    "그리로",
    "바로",
    "곧바로",
    "실제로",
    "반대로",
    "추가로",
    "기본적으로",
    "결과적으로",
}

# 한자 10단위
SINO_TENS = {
    "십": 10,
    "이십": 20,
    "삼십": 30,
    "사십": 40,
    "오십": 50,
    "육십": 60,
    "칠십": 70,
    "팔십": 80,
    "구십": 90,
}

# 한자 1단위
SINO_ONES = {
    "일": 1,
    "이": 2,
    "삼": 3,
    "사": 4,
    "오": 5,
    "육": 6,
    "칠": 7,
    "팔": 8,
    "구": 9,
}

# 순우리말 10단위
NATIVE_TENS = {
    "열": 10,
    "스물": 20,
    "스무": 20,
    "서른": 30,
    "마흔": 40,
    "쉰": 50,
    "예순": 60,
    "일흔": 70,
    "여든": 80,
    "아흔": 90,
}

# 순우리말 1단위
NATIVE_ONES = {
    "한": 1,
    "하나": 1,
    "두": 2,
    "둘": 2,
    "세": 3,
    "셋": 3,
    "네": 4,
    "넷": 4,
    "다섯": 5,
    "여섯": 6,
    "일곱": 7,
    "여덟": 8,
    "아홉": 9,
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", text)


def is_valid_age(age: int) -> bool:
    return 0 < age < 100


def extract_digit_age(text: str) -> Optional[int]:
    """
    숫자 나이 추출:
    23살, 23세, 만23세, 만 23세
    
    제외 내용:
    20세기
    """
    print("##### extract_digit_age start #####")
    match = re.search(r"(?:만\s*)?(\d{1,2})\s*(?:살|세)(?!기)", text)

    if not match:
        return None

    age = int(match.group(1))
    print("##### extract_digit_age end #####")
    return age if is_valid_age(age) else None


def parse_sino_number(normalized: str) -> Optional[int]:
    """
    한자식 숫자:
    십구, 이십삼, 삼십오, 사십구, 오십
    """
    print("##### parse_sino_number start #####")
    # 조합형 먼저: 이십삼, 삼십오
    for tens_word, tens_value in sorted(SINO_TENS.items(), key=lambda x: len(x[0]), reverse=True):
        for ones_word, ones_value in SINO_ONES.items():
            word = f"{tens_word}{ones_word}"

            if word in normalized:
                age = tens_value + ones_value
                print("##### parse_sino_number end #####")
                return age if is_valid_age(age) else None

    # 10단위 단독: 이십, 삼십, 십
    for tens_word, tens_value in sorted(SINO_TENS.items(), key=lambda x: len(x[0]), reverse=True):
        if tens_word in normalized:
            print("##### parse_sino_number end #####")
            return tens_value if is_valid_age(tens_value) else None

    # 1~9 단독은 나이로 보기 애매해서 제외
    print("##### parse_sino_number end #####")
    return None


def parse_native_number(normalized: str) -> Optional[int]:
    """
    고유어 숫자:
    열아홉, 스물셋, 스무살, 서른둘, 마흔다섯, 쉰여섯
    """
    print("##### parse_native_number start #####")
    # 조합형 먼저: 스물셋, 서른둘, 마흔다섯
    for tens_word, tens_value in sorted(NATIVE_TENS.items(), key=lambda x: len(x[0]), reverse=True):
        for ones_word, ones_value in sorted(NATIVE_ONES.items(), key=lambda x: len(x[0]), reverse=True):
            word = f"{tens_word}{ones_word}"

            if word in normalized:
                age = tens_value + ones_value
                print("##### parse_native_number end #####")
                return age if is_valid_age(age) else None

    # 10단위 단독: 열, 스물, 스무, 서른, 마흔, 쉰
    for tens_word, tens_value in sorted(NATIVE_TENS.items(), key=lambda x: len(x[0]), reverse=True):
        if tens_word in normalized:
            print("##### parse_native_number end #####")
            return tens_value if is_valid_age(tens_value) else None

    print("##### parse_native_number end #####")
    return None


def extract_korean_age(text: str) -> Optional[int]:
    """
    한글 나이 추출:
    스물셋
    스물 세
    스물세
    이십삼
    이십 삼
    열아홉
    십구
    마흔다섯
    쉰둘
    """
    print("##### extract_korean_age start #####")
    normalized = normalize_text(text)

    # 한자식 숫자 우선
    sino_age = parse_sino_number(normalized)
    if sino_age is not None:
        print("##### extract_korean_age end #####")
        return sino_age

    native_age = parse_native_number(normalized)
    if native_age is not None:
        print("##### extract_korean_age end #####")
        return native_age

    print("##### extract_korean_age end #####")
    return None


def extract_age(text: str) -> Optional[int]:
    """
    통합 나이 추출
    """
    print("##### extract_korean_age start #####")
    return extract_digit_age(text) or extract_korean_age(text)


def extract_region_text(text: str) -> Optional[str]:
    print("##### extract_region_text start #####")
    matches = REGION_PATTERN.findall(text)
    
    matches = [m for m in matches if m not in INVALID_REGION_WORDS]

    if not matches:
        print("##### extract_region_text end #####")
        return None

    # 주소 api 추가해서 필터링

    priority_suffixes = ["사거리", "역", "동", "구", "시", "군", "도"]

    for suffix in priority_suffixes:
        for match in matches:
            if match.endswith(suffix):
                print("##### extract_region_text end #####")
                return match

    print("##### extract_region_text end #####")
    return matches[0]


def classify_single(text: str, keyword_map: dict[str, list[str]]) -> Optional[str]:
    print("##### classify_single start #####")
    for label, keywords in keyword_map.items():
        for keyword in keywords:
            if keyword in text:
                print("##### classify_single end #####")
                return label
            
    print("##### classify_single end #####")
    return None


def classify_multi(text: str, keyword_map: dict[str, list[str]]) -> List[str]:
    print("##### classify_multi start #####")
    results = []

    for label, keywords in keyword_map.items():
        for keyword in keywords:
            if keyword in text:
                results.append(label)
                break


    print("##### classify_multi end #####")
    return results


def extract_by_rules(text: str) -> UserProfileSchema:
    print("##### extract_by_rules start #####")
    return UserProfileSchema(
        raw_text=text,
        age=extract_age(text),
        region_text=extract_region_text(text),
        employment_status=classify_single(text, EMPLOYMENT_KEYWORDS),
        education_status=classify_single(text, EDUCATION_KEYWORDS),
        housing_status=classify_single(text, HOUSING_KEYWORDS),
        income_status=classify_single(text, INCOME_KEYWORDS),
        policy_needs=classify_multi(text, POLICY_NEED_KEYWORDS),
        used_zero_shot=False,
    )