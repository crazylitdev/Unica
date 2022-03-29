import cv2
import json
import time
import random
import string
import base64
import qrcode
from pyDes import *

class QRCode:

    def __init__(self) -> None:
        self.password = "abc123abc123abc123abc123" #a 16 or 24 bit string
        self.cameraDevice = 0 #Can be changed for another camera device
        self.uniEncoding = "unicode_escape" #encoding used to convert the base64 string to unicode
        self.data = {} #output of read function

    def write(self, data:dict) -> str:
        'This function will encrypt and convert the object you pass in a QRCode and return the file path of the resulting image.'
        encryptedText = triple_des(self.password).encrypt(json.dumps(data), padmode=2)
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        encryptedText = base64.b64encode(encryptedText)
        encryptedText = encryptedText.decode(self.uniEncoding)
        qr.add_data(encryptedText)
        qr.make()
        timestamp = int(time.time())
        randomString = "".join(random.choices(string.ascii_uppercase + string.digits, k = 4))
        path = f"./Database/QROutput/QR{randomString}{timestamp}.png"
        qr.make_image().save(path)
        return path

    def read(self) -> dict:
        'This function will launch the camera, which can then be used to read QR codes, only QR codes created by this class can be read. The decrypted object will be returned.'
        camera = cv2.VideoCapture(self.cameraDevice)
        detector = cv2.QRCodeDetector()
        while True:
            _, image = camera.read()
            data, bbox, _ = detector.detectAndDecode(image)
            if bbox is not None:
                if data:
                    break
            if cv2.waitKey(1) == ord("q"):
                break
        camera.release()
        cv2.destroyAllWindows()
        data = data.encode(self.uniEncoding)
        data = base64.b64decode(data)
        decryptedData = json.loads(triple_des(self.password).decrypt(data, padmode=2))
        self.data = decryptedData
        return decryptedData

print(QRCode().read())