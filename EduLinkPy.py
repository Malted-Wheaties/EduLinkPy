import requests
import json
import base64
import os
import sys
from uuid import uuid4
from getpass import getpass
from PIL import Image
import ascii_magic

# Important variables;
"""
SCHOOL_CODE
SCHOOL_SERVER
SCHOOL_NAME
SCHOOL_LOGO_FILE_PATH
USERNAME
PASSWORD
AUTHTOKEN
GENDER
FORENAME
SURNAME
HOUSE_GROUP
FORM_GROUP
YEAR_GROUP
"""

def Flatten_JSON(_request):
        illegal_characters = [' ', '\n']
        request_clean = _request.text
        for illegal_character in illegal_characters:
                request_clean = request_clean.replace(illegal_character, '')

        request_JSON = json.loads(request_clean)

        return request_JSON


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

        try:
                check = Flatten_JSON(provisioning_request)["result"]["success"]
        except:
                exit(Flatten_JSON(provisioning_request)["error"]["message"])

        return Flatten_JSON(provisioning_request)["result"]["school"]["server"]

def School_Details(_school_svr, _process_logo):
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

        try:
                check = Flatten_JSON(details_request)["result"]["success"]
        except:
                exit(Flatten_JSON(details_request)["error"]["message"])

        school_name = Flatten_JSON(details_request)["result"]["establishment"]["name"]

        if _process_logo is True:
                school_logo_base64 = Flatten_JSON(details_request)["result"]["establishment"]["logo"]
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


def Set_Account_Info(_usr, _pwd, _school_svr, _process_photo):
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
        login_body = json.dumps(login_body_raw)
        login_headers = {"Content-Type":"application/json;charset=utf-8"}
        login_request = requests.post(login_url, data=login_body, headers=login_headers) # type requests.models.Response
        
        try:
                check = Flatten_JSON(login_request)["result"]["success"]
        except:
                exit(Flatten_JSON(login_request)["error"]["message"])

        with open ("login-output.txt", "w+") as f:
                f.write(login_request.text)
        f.close()
    

        AUTHTOKEN = Flatten_JSON(login_request)["result"]["authtoken"]

        GENDER = Flatten_JSON(login_request)["result"]["user"]["gender"]
        FORENAME = Flatten_JSON(login_request)["result"]["user"]["forename"]
        SURNAME = Flatten_JSON(login_request)["result"]["user"]["surname"]
        full_name = FORENAME + " " + SURNAME

        if _process_photo:
                portrait_base64 = Flatten_JSON(login_request)["result"]["user"]["avatar"]["photo"]
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

        year_group_id = Flatten_JSON(login_request)["result"]["user"]["year_group_id"]
        form_group_id = Flatten_JSON(login_request)["result"]["user"]["form_group_id"]
        house_id = Flatten_JSON(login_request)["result"]["user"]["community_group_id"]
        
        year_groups_list = Flatten_JSON(login_request)["result"]["establishment"]["year_groups"]
        for obj in year_groups_list:
                if obj["id"] == year_group_id:   
                        YEAR_GROUP = obj["name"]
                        YEAR_GROUP = YEAR_GROUP.replace("Year", "Year ")

        form_groups_list = Flatten_JSON(login_request)["result"]["establishment"]["form_groups"]
        for obj in form_groups_list:
                if obj["id"] == form_group_id:
                        FORM_GROUP = obj["name"]

        house_groups_list = Flatten_JSON(login_request)["result"]["establishment"]["community_groups"]
        for obj in house_groups_list:
                if obj["id"] == house_id:
                        HOUSE_GROUP = obj["name"]

        return AUTHTOKEN, GENDER, FORENAME, SURNAME, full_name, YEAR_GROUP, FORM_GROUP, HOUSE_GROUP


SCHOOL_CODE = input("Enter your school code: ")

SCHOOL_SERVER = School_Server(SCHOOL_CODE)

SCHOOL_NAME = School_Details(SCHOOL_SERVER, False)

USERNAME = input("Enter your EduLink username: ")
PASSWORD = getpass("Enter your EduLink password: ")
AUTHTOKEN, GENDER, FORENAME, SURNAME, full_name, YEAR_GROUP, FORM_GROUP, HOUSE_GROUP = Set_Account_Info(USERNAME, PASSWORD, SCHOOL_SERVER, False)

print(full_name + ": " + GENDER)
print(FORM_GROUP + " (" + YEAR_GROUP + " " + HOUSE_GROUP + ")")