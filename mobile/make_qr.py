import qrcode
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data('exp://')
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save('expo_qr_new.png')
