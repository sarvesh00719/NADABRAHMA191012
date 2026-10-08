import requests

url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"
headers = {
    "xi-api-key": "sk_c3e2cf81649e2c281bf59ae4ea4db19e0ed0dbfc07bbf80a",
    "Content-Type": "application/json"
}
data = {
    "text": "Hello world",
    "model_id": "eleven_turbo_v2_5",
    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
}

response = requests.post(url, headers=headers, json=data)
print("Status Code:", response.status_code)
if response.status_code != 200:
    print("Error:", response.text)
else:
    print("Success: Audio data received.")
