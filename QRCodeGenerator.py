import pyqrcode
from pyzbar.pyzbar import decode
from PIL import Image


class QRCodeGenerator:

    def __init__(self, frames):
        self.frames = frames

    def generate_qr_codes(self):
        print('Beginning QR-Code generation...')
        for frame in range(self.frames):
            qr = pyqrcode.create(frame + 1)
            img_name = 'Images/QR_Code_Frame_' + str(frame + 1) + '.png'
            qr.png(img_name, scale=5)
        print('QR-Codes have been generated for ' + str(frame + 1) + ' frames.')

