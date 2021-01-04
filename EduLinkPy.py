import requests
import json
import base64
import os
from uuid import uuid4
from getpass import getpass
from PIL import Image
import ascii_magic
from dotenv import load_dotenv

# Important variables;
"""
SCHOOL_CODE
s_SCHOOL_SERVER
s_SCHOOL_NAME
SCHOOL_LOGO_FILE_PATH
USERNAME
PASSWORD
AUTHTOKEN
GENDER
FORENAME
SURNAME
"""

SCHOOL_CODE = input("Enter your school code: ")

def Flatten_JSON(_unflat_response_json):
        flat_json = {}
        flat_json[''[:-1]] = _unflat_response_json
        for text in flat_json:
                print(text)
                text.replace(' ', '')
        return flat_json

def Find_Info(_request, _query, _index_add = 2): #Because the API returns the info as a string, not JSON, it has indents and newlines to make it look like JSON, which makes it harder to parse. I used a lazier method of picking through the response to get the query's content.
        request_text = _request.text
        request_text_split = request_text.split('"')
        for text in request_text_split:
                if _query in text.lower():
                        index = request_text_split.index(text) + _index_add # +0 would be the label, +1 would be a colon and a space, +2 gives the content corresponding to the query
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

        print(Flatten_JSON(provisioning_request.text))
        if "false" in Find_Info(provisioning_request, "success", 1).lower():
               exit(Find_Info(provisioning_request, "error"))

        return Find_Info(provisioning_request, "server")


def School_Details(_school_svr):
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
        if "false" in Find_Info(details_request, "success", 1).lower():
                exit(Find_Info(details_request, "error"))
        school_name = Find_Info(details_request, "name")

        school_logo_base64 = Find_Info(details_request, "logo")
        school_logo_64 = base64.b64decode(school_logo_base64) # type bytes
        file_directory = os.getcwd() + "/"
        file_name = school_name + " Logo.png"
        SCHOOL_LOGO_FILE_PATH = file_directory + file_name

        with open (SCHOOL_LOGO_FILE_PATH, "wb") as f:
                f.write(school_logo_64)
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

        school_logo_ascii = ascii_magic.from_image_file(SCHOOL_LOGO_FILE_PATH)
        ascii_magic.to_terminal(school_logo_ascii)

        return school_name


def Set_Account_Info(_usr, _pwd, _school_svr):
        login_url = _school_svr + "?method=EduLink.Login"
        login_body_raw = {
                "jsonrpc":"2.0",
                "method":"EduLink.Login",
                "params":{
                        "from_app":False,
                        "ui_info":{
                                "format":2,
                                "version":"0.5.114",
                                "git_sha":str(uuid4())
                        },
                        "fcm_token_old":"none",
                        "username":_usr,
                        "password":_pwd,
                        "establishment_id":"2"
                },
                "uuid":str(uuid4()),
                "id":"1"
        }
        login_body = json.dumps(login_body_raw) # type str
        login_headers = {"Content-Type":"application/json;charset=utf-8"}
        login_request = requests.post(login_url, data=login_body, headers=login_headers) # type requests.models.Response
        if "false" in Find_Info(login_request, "success", 1):
               exit(Find_Info(login_request, "error"))

        
        AUTHTOKEN = Find_Info(login_request, "authtoken")
        
        GENDER = Find_Info(login_request, "gender")
        FORENAME = Find_Info(login_request, "forename")
        SURNAME = Find_Info(login_request, "surname")
        full_name = FORENAME + " " + SURNAME
        print("Hello, " + full_name)


        portrait_base64 = Find_Info(login_request, "photo")
        portrait_64 = base64.b64decode(portrait_base64) # type bytes
        file_directory = os.getcwd() + "/"
        file_name = full_name + " Portrait.png"
        PORTRAIT_FILE_PATH = file_directory + file_name
        print(PORTRAIT_FILE_PATH)

        with open (PORTRAIT_FILE_PATH, "wb") as f:
                f.write(portrait_64)
        f.close()

        portrait_ascii = ascii_magic.from_image_file(PORTRAIT_FILE_PATH)
        ascii_magic.to_terminal(portrait_ascii)


s_SCHOOL_SERVER = School_Server(SCHOOL_CODE)
s_SCHOOL_NAME = School_Details(s_SCHOOL_SERVER)

USERNAME = input("Enter your EduLink username: ")
PASSWORD = getpass("Enter your EduLink password:")
Set_Account_Info(USERNAME, PASSWORD, s_SCHOOL_SERVER)