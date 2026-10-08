import requests

url = "https://api.elevenlabs.io/v1/voices"
headers = {
    "xi-api-key": "sk_c3e2cf81649e2c281bf59ae4ea4db19e0ed0dbfc07bbf80a"
}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.text)
