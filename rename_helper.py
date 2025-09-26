import requests

API_KEY = "AIzaSyARfFeM-9S8fW6n7_7WfyyUKQ9fNSwszX0"
CX = "f76903d7b221c4639"

def fetch_movie_name(code: str) -> str:
    """
    输入番号 (如 SSIS-129)，从 javdb 搜索并返回电影标题
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": f"{code} site:javdb.com"
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return code

    data = res.json()
    if "items" in data and len(data["items"]) > 0:
        title = data["items"][0]["title"]
        # 清洗掉尾巴
        for junk in ["- JavDB", "| JavDB", "JavDB"]:
            title = title.replace(junk, "")
        return title.strip()
    else:
        print(f"⚠️ 未找到标题: {code}")
        return code

if __name__ == "__main__":
    test_codes = ["SSIS-129", "IPX-967", "ABW-123"]
    for code in test_codes:
        print(f"{code} → {fetch_movie_name(code)}")
