# EduLinkPy

## Each request method contains a combination of the following;

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