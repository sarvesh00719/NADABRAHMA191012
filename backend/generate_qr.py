import qrcode
import sys

# Expo URL for the new IP
url = 'exp://10.85.34.148:8081'

qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color='black', back_color='white')
img.save(r'C:\Users\Sarvesh\.gemini\antigravity\brain\db4cb2cd-1921-4ea2-bf59-be1ec7bd7358\expo_qr_new_ip.png')

md_content = f'''# Expo QR Code

Your computer's IP address has changed. Scan this new QR code using your phone's Camera (iOS) or Expo Go app (Android) to connect to the server:

![Expo QR](file:///C:/Users/Sarvesh/.gemini/antigravity/brain/db4cb2cd-1921-4ea2-bf59-be1ec7bd7358/expo_qr_new_ip.png)

*Server IP: 10.85.34.148:8081*
'''
with open(r'C:\Users\Sarvesh\.gemini\antigravity\brain\db4cb2cd-1921-4ea2-bf59-be1ec7bd7358\expo_qr_new_ip.md', 'w') as f:
    f.write(md_content)
