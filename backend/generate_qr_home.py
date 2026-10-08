import qrcode
import sys

url = 'exp://192.168.1.6:8081'

qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color='black', back_color='white')
img.save(r'C:\Users\Sarvesh\.gemini\antigravity\brain\db4cb2cd-1921-4ea2-bf59-be1ec7bd7358\expo_qr_home.png')
