import requests

def send_result_to_server(result, url):
    try:
        response = requests.post(url, json=result)
        print(f"[LOG] 외부 서버 응답: {response.status_code} {response.text}")
        return response.status_code, response.text
    except Exception as e:
        print(f"[ERROR] 외부 서버 전송 실패: {e}")
        return None, str(e)