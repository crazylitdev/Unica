
from Database.DBIntegration import Blockchain, mongoDB
import json
import random
import string
import base64
from pyDes import *
from Functions.OTP import OTP
from Functions.QR import QRCode
from PIL import ImageTk, Image
from tkinter import *


class Normal(QRCode):

    def __init__(self, phone:int) -> None:
        super().__init__()
        self.phone = phone
        self.user = mongoDB().viewUser(self.phone)

    def login(self) -> bool:
        otp = OTP().sendOTP(self.phone)
        userInput = input("Please Enter The OTP : ")
        if int(userInput) == otp:
            if self.user is None:
                primaryKey = int("".join(random.choices(string.digits, k = 16)))
                name = input("Enter Your Name : ")
                self.user = {"phone": self.phone, "accounts": [{"primaryKey": primaryKey, "name": name}]}
            return True
        else:
            return False

    def writeQR(self) -> str:
        path = self.write(self.user)
        return path

    def viewQR(self, path:str) -> None:
        root = Tk()   
        root.geometry("400x400")  
        image = ImageTk.PhotoImage(image=Image.open(path)) 
        Label(root, image = image).place(x = 15, y = 15)
        root.mainloop()

    def main(self):
        if self.login() is True:
            path = self.writeQR()
            self.viewQR(path)
        else:
            print("Invalid OTP.")


class Admin:

    def __init__(self) -> None:
        self.password = "abc123abc123abc123abc123"
        self.uniEncoding = "unicode_escape"

    def readQR(self) -> None:
        data = QRCode().read()
        return data

    def addUser(self, primaryKey:int) -> None:
        data = {"data": [primaryKey]}
        encryptedText = triple_des(self.password).encrypt(json.dumps(data), padmode=2)
        encryptedText = base64.b64encode(encryptedText)
        encryptedText = encryptedText.decode(self.uniEncoding)
        print(encryptedText, type(encryptedText))
        Blockchain().insertUser(1, encryptedText)

    def checkUser(self, primaryKey:int) -> bool:
        data = Blockchain().viewUser(1)
        data = data.encode(self.uniEncoding)
        data = base64.b64decode(data)
        decryptedData = json.loads(triple_des(self.password).decrypt(data, padmode=2))
        if primaryKey in decryptedData["data"]:
            return True
        else:
            return False

    def main(self):
        primaryKey = self.readQR()
        if self.checkUser(primaryKey) is True:
            print("User Allowed")
        else:
            print("no")


