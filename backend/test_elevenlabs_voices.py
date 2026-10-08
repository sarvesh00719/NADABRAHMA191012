import requests

url = "https://api.elevenlabs.io/v1/voices"
headers = {
    "xi-api-key": "sk_c3e2cf81649e2c281bf59ae4ea4db19e0ed0dbfc07bbf80a"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    voices = response.json().get('voices', [])
    for v in voices:
        print(f"Name: {v['name']}, ID: {v['voice_id']}, Category: {v['category']}")
else:
    print("Error:", response.text)
