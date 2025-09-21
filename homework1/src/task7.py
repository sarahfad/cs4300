import requests

def get_status(url):
    """Uses the requests library to get an http status code"""
    response = requests.get(url)
    response.raise_for_status()
    return response.status_code

def get_encoding(url):
    """Uses the requests library to get the response text encoding"""
    response = requests.get(url)
    response.raise_for_status()
    return response.encoding

def post_json(url, payload):
    """Sends a JSON payload with POST and returns the parsed JSON response"""
    resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    print(get_status("https://httpbin.org/status/200"))
    print(get_encoding("https://httpbin.org/encoding/utf8"))
    print(post_json("https://httpbin.org/post", {"hello": "world"}))