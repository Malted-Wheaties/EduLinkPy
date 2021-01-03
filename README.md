# EduLinkPy

---

## Variable naming

Important variables are commented at the top in upper case.
Of which are recieved by the server are preceeded with `_s`.
Argument variables are preceeded with `_`.

## Each request method may contain;

### url
The school server (usually in the format https://_schoolcode_.edulinkone.com/api/) is combined with the method name to create a url to which the request will be sent.
Is of type `string`

### body_raw
The information to be sent in the POST request.
It has been included instead of a flattened JSON string for readability
Is of type `dict`

### body
Utilises `json.dumps()` to serialize `body_raw` `dict` to a flat, JSON formatted `str`.
Is sent in the POST request.

### headers
The header to be sent with 
Is of type `dict`

### request
Uses `requests.post()` to send a HTTP POST request to **url** containing **body** and **headers**

## Edulink API methods

`EduLink.FromCode` amongst other information, returns;
* The school server (`s_SCHOOL_SERVER`)

`Edulink.SchoolDetails` amongst other information, returns;
* The name of the school (`s_SCHOOL_NAME`)
* Google sign in URL
* The School logo encoded in base64

`Edulink.Login` amongst other information, returns;
*  The name of the school
* The school logo encoded in base64
* The session's account authtoken
* User information, including;

    * Account ID
    * Gender
    * Forename
    * Surname
    * username
    * Portrait photo
    
* Menu items (timetable, documents, catering, homework etc.)
* Whether the user can create messages to send
