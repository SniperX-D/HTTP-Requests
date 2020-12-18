# HTTP-Requests
Parsing and sorting HTTP requests and trier responses from requests.txt file.
for requests the script prints:
1. endpoint
2. method
3. the arguments from the request in a dictionary

for responses the script prints the payload, and in the case of JSON it parses it into a dictionary.

## Usage:
1. add requests to requests.txt with a header ```Req_N:``` or ```Res_N:```
2. add CR-LF of 80 "-" at the end of each request or response
3. run by typing ```python service.py```

## requests.txt:
includes requests and responses from https://jsonplaceholder.typicode.com/ and requests from my personal honey-pot

## Output for requests.txt:
```bash
root@kali:~/Test-interview$ python service.py 
------------------------------http request 1 ------------------------------
Method: GET
endpoint: /typicode/demo/comments
arguments: {'username': 'hello', 'name': 'wow'}


------------------------------http response 1------------------------------
response json payload :
[{u'body': u'some comment', u'postId': 1, u'id': 1}, {u'body': u'some comment', u'postId': 1, u'id': 2}]


------------------------------http request 2 ------------------------------
Method: GET
endpoint: /typicode/demo/comments
arguments: {}


------------------------------http response 2------------------------------
response json payload :
[{u'body': u'some comment', u'postId': 1, u'id': 1}, {u'body': u'some comment', u'postId': 1, u'id': 2}]


------------------------------http request 3 ------------------------------
Method: GET
endpoint: /typicode/demo/profile
arguments: {}


------------------------------http response 3------------------------------
response json payload :
{u'name': u'typicode'}


------------------------------http request 4 ------------------------------
Method: GET
endpoint: /typicode/demo/comments
arguments: {'id': '1'}


------------------------------http response 4------------------------------
response json payload :
[{u'body': u'some comment', u'postId': 1, u'id': 1}]


------------------------------http request 5 ------------------------------
Method: GET
endpoint: /
arguments: {'XDEBUG_SESSION_START': 'phpstorm'}


------------------------------http request 6 ------------------------------
Method: POST
endpoint: /boaform/admin/formLogin
arguments: {'username': 'admin', 'psd': 'Feefifofum'}


------------------------------http request 7 ------------------------------
Method: POST
endpoint: /api/jsonws/invoke
arguments: {u'test': u'testing...'}

```
