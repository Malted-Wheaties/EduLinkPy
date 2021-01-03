import requests
import json
import base64
import os
from uuid import uuid4

# Important variables;
"""
SCHOOL_CODE
s_SCHOOL_SERVER
s_SCHOOL_NAME
SCHOOL_LOGO_FILE_PATH
USERNAME
PASSWORD
AUTHTOKEN
"""

SCHOOL_CODE = input("Enter your school code\t")
USERNAME  = input("Enter your EduLink username\t")
PASSWORD  = input("Enter your EduLink password\t")

#Because the API returns the info as a string, not JSON, it has indents and newlines to make it look like JSON, which makes it harder to parse. I used a lazy method of picking through the response to get the school server.
def Find_Info(_request, _query):
        request_text = _request.text
        request_text_split = request_text.split('"')
        for text in request_text_split:
                if _query in text:
                        index = request_text_split.index(text)
                        return request_text_split[index]
        return "QUERY" + _query + " NOT FOUND"


def School_Server(_school_code):
        provisioning_url = "https://provisioning.edulinkone.com/?method=School.FromCode/"
        provisioning_body_raw = {
                "jsonrpc":"2.0",
                "method":"School.FromCode",
                "params":{
                        "code":(_school_code)
                },
                "uuid":str(uuid4()),
                "id":"1"
        }
        provisioning_body = json.dumps(provisioning_body_raw)
        provisioning_request = requests.post(provisioning_url, data=provisioning_body) # type requests.models.Response

        return Find_Info(provisioning_request, "http")


def School_Details(_school_svr, _save_logo):
        details_url = _school_svr + "?method=EduLink.SchoolDetails"
        details_body_raw = {
                "id":"1",
                "jsonrpc":"2.0",
                "method":"EduLink.SchoolDetails",
                "params":{
                "establishment_id":"2",
                "from_app":False
                },
                "uuid":str(uuid4())
        }
        details_body = json.dumps(details_body_raw)
        details_headers = {"Content-Type":"application/json;charset=utf-8"}
        details_request = requests.post(details_url, data=details_body, headers=details_headers) # type requests.models.Response

        school_name = Find_Info(details_request, "name")

        if (_save_logo):

                #region Save Image
                school_logo_base64 = Find_Info(details_request, "logo")
                school_logo = base64.b64decode(school_logo_base64) # type bytes
                file_directory = os.getcwd() + "/"
                file_name = school_name + " Logo.png"
                SCHOOL_LOGO_FILE_PATH = file_directory + file_name
                with open (SCHOOL_LOGO_FILE_PATH, "wb") as f:
                        f.write(school_logo)
                f.close()

                #To return converted image without saving;
                """
                from PIL import Image
                import cv2

                # Take in base64 string and return cv image
                def stringToRGB(school_logo_base64):
                school_logo = base64.b64decode(str(school_logo_base64))
                image = Image.open(io.BytesIO(school_logo))
                return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
                """
                #endregion

        return school_name


def Authtoken(_usr, _pwd, _school_svr):
        login_url = _school_svr + "?method=EduLink.Login"
        login_body_raw = {
                "jsonrpc":"2.0",
                "method":"Edulink.Login",
                "params":{
                        "from_app":False,
                        "ui_info":{
                                "format":2,
                                "version":"0.5.114",
                                "git_sha":"128522674"
                        },
                        "fcm_token_old":"none",
                        "username":_usr,
                        "password":_pwd,
                        "establishment_id":"2"
                },
                "uuid":"128522674",#str(uuid4()),
                "id":"1"
        }
        login_body = json.dumps(login_body_raw) # type str
        login_headers = {"Content-Type":"application/json;charset=utf-8","User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}
        login_request = requests.post(login_url, data=login_body, headers=login_headers) # type requests.models.Response

        ##### TEMPORARY #####
        with open("/home/ben/dev/edulink/login.txt", "w+") as f:
                f.write(login_request.text)
        f.close()

        return Find_Info(login_request, "authtoken")


s_SCHOOL_SERVER = School_Server(SCHOOL_CODE)
s_SCHOOL_NAME = School_Details(s_SCHOOL_SERVER, True)
AUTHTOKEN = Authtoken(USERNAME, PASSWORD, s_SCHOOL_SERVER)
print(s_SCHOOL_SERVER)
print(s_SCHOOL_NAME)
print(AUTHTOKEN)