import uvicorn
from fastapi import FastAPI, Query
import requests

app = FastAPI()

JUSO_API_KEY = "api_key"
REST_API_KEY = "api_key"


@app.get("/address/search")
def search_address(keyword: str = Query(...)):
    url = "https://business.juso.go.kr/addrlink/addrLinkApi.do"

    params = {
        "confmKey": JUSO_API_KEY,
        "currentPage": 1,
        "countPerPage": 10,
        "keyword": keyword,
        "resultType": "json",
    }

    print(f"##### params:{params} #####")
    response = requests.get(url, params=params, timeout=5)
    # print(f"##### response:{response} #####")
    print(f"##### status: {response.status_code} #####")
    print(f"##### text: {response.text} #####")
    # response.raise_for_status()
    

    data = response.json()

    print(f"##### data:{data} #####")
    return {
        "success": True,
        "keyword": keyword,
        "data": data.get("results", {}).get("juso", []),
        "common": data.get("results", {}).get("common", {}),
    }
    
@app.get("/address/search2")
def search_address(keyword: str = Query(...)):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    
    print(f"##### rest_api_key : {REST_API_KEY} #####")
    
    headers = {
        "Authorization": f"KakaoAK {REST_API_KEY}"
    }

    params = {
        "query": keyword,
        "page": 1,
        "size": 5
    }

    # print(f"##### params:{params} #####")
    response = requests.get(url, headers=headers, params=params)
    # print(f"##### response:{response} #####")
    # print(f"##### status: {response.status_code} #####")
    # print(f"##### text: {response.text} #####")
    response.raise_for_status()

    data = response.json()

    # print(f"##### data:{data} #####")   
    
    result = []
    
    for place in data["documents"]:
        res_place = {}
        
        if place["address_name"] :
            res_place["address_name"] = place["address_name"]
            
        if place["place_name"] :
            res_place["place_name"] = place["place_name"]
            
        result.append(res_place)
        
    return {
        "success": True,
        "keyword": keyword,
        "data_list" : result
    }