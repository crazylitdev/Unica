import time
import random
import string
import requests
import json
import base64
from seleniumwire import webdriver

class Verify:
    
    def __init__(self) -> None:
        self.covidBearer = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiI1MjVjMmZmZC1jMGY4LTRiOGItODRjYy1iZjY4YmQ5M2JmOGMiLCJ1c2VyX2lkIjoiNTI1YzJmZmQtYzBmOC00YjhiLTg0Y2MtYmY2OGJkOTNiZjhjIiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo5Mjg0ODkzNTg1LCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjI4OTQ1OTUxNjcxNDMwLCJzZWNyZXRfa2V5IjoiYjVjYWIxNjctNzk3Ny00ZGYxLTgwMjctYTYzYWExNDRmMDRlIiwic291cmNlIjoiY293aW4iLCJ1YSI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS85OC4wLjQ3NTguMTAyIFNhZmFyaS81MzcuMzYiLCJkYXRlX21vZGlmaWVkIjoiMjAyMi0wMy0yNVQyMzozNDoxMS43MDRaIiwiaWF0IjoxNjQ4MjUxMjUxLCJleHAiOjE2NDgyNTIxNTF9.ijPDB0KJ3aU_DF3caqpIjAcpffqkc3NT6cfeEciCaMA"
        self.covidSecret = "U2FsdGVkX18jFT4mFXSA5lY6gB3O/azBho6fbJF14DhwE2pt9Bow88lmewlNEMEOJzrp9haa6sg/+rXJlo3RoQ=="
        self.cookie = ""
        self.data = ""

    def covidVaccination(self, mobile:int) -> dict:
        "This function inputs user's mobile number and returns his vaccination details."
        url = "https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP"
        headers = {
            "authority": "cdn-api.co-vin.in",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            "accept": "application/json, text/plain, */*",
            "content-type": self.covidBearer,
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "origin": "https://selfregistration.cowin.gov.in",
            "referer": "https://selfregistration.cowin.gov.in/"
        }
        data = '{"secret":self.covidSecret,"mobile":mobile}'
        response = requests.post(url, headers=headers, data=data)
        response = response.text
        response = json.loads(response)
        return response

    def keepAlive(self, request):
        request.headers['Connection'] = 'keep-alive'

    def interceptor(self, request):
        request.headers["Content-Type"] = "application/x-www-form-urlencoded"
        request.headers["Cookie"] = self.cookie
        request.body = self.data.encode("utf-8")

    def aadharCookie(self) -> str:
        "This function will use selenium-wire to fetch an Aadhaar Session."
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(seleniumwire_options={'ca_cert': 'ca.crt'}, chrome_options=chrome_options)
        self.driver.request_interceptor = self.keepAlive
        self.driver.get("https://myaadhaar.uidai.gov.in/")
        button = self.driver.find_element_by_class_name("button_btn__1dRFj")
        button.click()
        request = self.driver.wait_for_request('https://tathya.uidai.gov.in/login')
        for request in self.driver.requests:
            if request.url == "https://tathya.uidai.gov.in/styles/style.css":
                self.cookie = request.headers["Cookie"]

    def aadharCaptcha(self) -> dict:
        "This function will generate the captcha, store it locally and returns the path and the transaction id." 
        url = "https://tathya.uidai.gov.in/generateCaptcha"
        cookie = self.cookie
        headers = {
            "Connection": "keep-alive",
            "Cookie": cookie,
            "dnt": "1",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Host": "tathya.uidai.gov.in",
            "Referer": "https://tathya.uidai.gov.in/login",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response = response.text
        response = json.loads(response)
        message = json.loads(response["message"])
        captcha = message["imageBase64"]
        transactionID = message["transactionId"]
        timestamp = int(time.time())
        randomString = "".join(random.choices(string.ascii_uppercase + string.digits, k = 4))
        path = f"./Database/Captcha/{randomString}{timestamp}.png"
        captchaFile = open(path, "wb")
        captchaFile.write(base64.decodebytes(bytes(captcha, 'utf-8')))
        captchaFile.close()
        print(path)
        data = {"path": path, "transactionID": transactionID}
        return data

    def aadharOTP(self, uid:int, captcha:str, transactionID:str) -> bool:
        "This function inputs user's aadhar number, catpcha answer and transaction id, and if OTP is sucessfully sent, it return true else false."
        url = "https://tathya.uidai.gov.in/generateOTPForOAuth"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "Content-type": "application/json",
            "dnt": "1",
            "Origin": "https://tathya.uidai.gov.in",
            "Referer": "https://tathya.uidai.gov.in/login",
            "Cookie": self.cookie
        }
        data = '{"uid":"' + str(uid) + '","captcha":"' + captcha + '", "captchaTxnId":"' + transactionID + '"}'
        response = requests.post(url, headers=headers, data=data)
        response = response.text
        response = json.loads(response)
        if response["status"] == True:
            return True
        else:
            return False

    def aadharLogin(self, uid:int) -> None:
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(seleniumwire_options={'ca_cert': 'ca.crt'}, chrome_options=chrome_options)
        # self.data = f"_csrf=112ce267-4d11-4123-96a4-34836f527ddf&uid={uid}&captcha={captcha}&otp={otp}&submit=Login"
        # self.driver.request_interceptor = self.interceptor
        self.driver.request_interceptor = self.keepAlive
        self.driver.get("https://myaadhaar.uidai.gov.in/")
        button = self.driver.find_element_by_class_name("button_btn__1dRFj")
        button.click()
        request = self.driver.wait_for_request('https://tathya.uidai.gov.in/login')
        for request in self.driver.requests:
            if request.url == "https://tathya.uidai.gov.in/styles/style.css":
                self.cookie = request.headers["Cookie"]
        time.sleep(2)
        captchaQ = self.driver.find_element_by_id("captcha_block")
        # captcha = captchaQ.get_attribute("src")
        print(captchaQ)
        return
        self.driver.wait_for_request('')
        # print(self.aadharCaptcha())
            # if request.url == "https://tathya.uidai.gov.in/generateCaptcha":
            #     response = request.response.body
            #     print(response)
                # response = json.loads(response)
                # message = json.loads(response["message"])
                # captcha = message["imageBase64"]
                # timestamp = int(time.time())
                # randomString = "".join(random.choices(string.ascii_uppercase + string.digits, k = 4))
                # path = f"./Database/Captcha/{randomString}{timestamp}.png"
                # captchaFile = open(path, "wb")
                # captchaFile.write(base64.decodebytes(bytes(captcha, 'utf-8')))
                # captchaFile.close()
                # print(path)
        uidField = self.driver.find_element_by_id("uid")
        uidField.send_keys(uid)
        captchaField = self.driver.find_element_by_id("captcha")
        captchaValue = input("Enter The Captcha :")
        captchaField.send_keys(captchaValue)
        sendOtp = self.driver.find_element_by_id("submit-btn")
        sendOtp.click()
        self.driver.wait_for_request("https://tathya.uidai.gov.in/generateOTPForOAuth")

        # for request in self.driver.requests:
        #     if request.url == "https://tathya.uidai.gov.in/ssupService/api/demographics/request/v4/profile":
        #         print(request.response.body)

    def aadharVerification(self, uid:int) -> dict:
        "This function inputs user's aadhar number, it verifies his identity and if everything goes well, it returns true else false."
        transactionID = self.aadharCaptcha()["transactionID"]
        captcha = input("Enter The Captcha :")
        if self.aadharOTP(uid, captcha, transactionID) is True:
            otp = input("Enter The OTP :")
            self.aadharLogin(uid, captcha, otp)
        else:
            data = {"status": False, "reason": "Captcha Error"}
            return data

Verify().aadharLogin(896442542348)
