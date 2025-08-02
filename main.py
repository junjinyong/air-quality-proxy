from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests, urllib.parse, os

app = FastAPI()

@app.get("/getAirQuality")
def get_air_quality(stationName: str = "종로구"):
    api_key = os.getenv("API_KEY")
    if not api_key:
        return JSONResponse(content={"error": "API_KEY not set"}, status_code=500)

    base_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"
    encoded_key = urllib.parse.quote(api_key)

    params = {
        "serviceKey": encoded_key,
        "returnType": "json",
        "numOfRows": "1",
        "pageNo": "1",
        "stationName": stationName,
        "dataTerm": "DAILY",
        "ver": "1.0"
    }

    try:
        res = requests.get(base_url, params=params)
        item = res.json()["response"]["body"]["items"][0]
        return {
            "time": item["dataTime"],
            "pm25": item["pm25Value"],
            "pm10": item["pm10Value"]
        }
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

