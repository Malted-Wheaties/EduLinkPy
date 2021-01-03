import requests
import json
from password import password
from uuid import uuid4
import base64
import os

SCHOOLCODE = "calday"


def Find_Info(request, query):
        request_text = request.text
        request_text_split = request_text.split('"') # type list
        for text in request_text_split:
                if query in text:
                        index = request_text_split.index(text)
        return request_text_split[index]

########## PROVISIONING INFO ##########

provisioning_url = "https://provisioning.edulinkone.com/?method=School.FromCode/"
provisioning_body_raw = { # type dict
        "jsonrpc":"2.0",
        "method":"School.FromCode",
        "params":{
                "code":(SCHOOLCODE)
        },
        "uuid":str(uuid4()),
        "id":"1"
}
provisioning_body = json.dumps(provisioning_body_raw) # type str, {"jsonrpc": "2.0", "method": "School.FromCode", "params": {"code": "calday"}, "uuid": "e51cbfe8-bc37-4c71-85ba-356a2e2ede2f", "id": "1"}

provisioning_request = requests.post(provisioning_url, data=provisioning_body) # type requests.models.Response
provisioning_request_text = provisioning_request.text # type str
"""
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "success": true,
    "school": {
      "server": "https://calday.edulinkone.com/api/",
      "school_id": 2
    }
  }
}
"""

#Because the API returns the info as a string, not JSON, it has indents and newlines to make it look like JSON, which makes it harder to parse. I used a lazy method of picking through the response to get the school server.


SchoolServer = Find_Info(provisioning_request, "http")
print(SchoolServer)



########## SCHOOL DETAILS ##########

details_url = SchoolServer + "?method=EduLink.SchoolDetails"
details_body_raw = {
        "id":"1",
        "jsonrpc":"2.0",
        "method":"EduLink.SchoolDetails",
        "params":{
            "establishment_id":"2",
            "from_app":"false"
        },
        "uuid":str(uuid4())
}
details_body = json.dumps(details_body_raw) # type str
details_headers = {"Content-Type":"application/json;charset=utf-8"}

details_request = requests.post(details_url, data=details_body, headers=details_headers) # type requests.models.Response

SCHOOL_NAME = Find_Info(details_request, "name")

school_logo_base64 = Find_Info(details_request, "logo")
school_logo = base64.b64decode(school_logo_base64) # type bytes
file_directory = os.getcwd() + "/"
file_name = "school_logo.png"
FILE_PATH = file_directory + file_name
with open (FILE_PATH, "wb") as f:
        f.write(school_logo)
f.close()

#To return converted image without saving;
"""
from PIL import Image
import cv2

# Take in base64 string and return cv image
def stringToRGB(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    image = Image.open(io.BytesIO(imgdata))
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
"""



########## LOGIN SECTION ##########

login_url = SchoolServer + "?method=EduLink.Login"
login_header = { #type dict
        "Content-Type":"application/json;charset=utf-8"
}
login_body_raw = { # type dict
        "jsonrpc":"2.0",
        "method":"Edulink.Login",
        "params":{
                "from_app":"false",
                "ui_info":{
                        "format":2,
                        "version":"0.5.114",
                        "git_sha":"e17855df1f830849539d84e39fe7ea8388da285d"
                        
                },
                "fcm_token_old":"none",
                "username":"dixonbw",
                "password":password,
                "establishment_id":"2"
                
        },
        "uuid":str(uuid4()),
        "id":"1"
}
login_body = json.dumps(login_body_raw) # type str
login_headers = {"Content-Type":"application/json;charset=utf-8"}

login_request = requests.post(login_url, data=login_body, headers=login_headers) # type requests.models.Response

with open("/home/ben/dev/edulink/login.txt", "w+") as f:
        f.write(login_request.text)
f.close()

AUTHTOKEN = Find_Info(login_request, "authtoken")