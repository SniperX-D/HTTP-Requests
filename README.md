# HTTP-Requests
Parsing and sorting HTTP requests and trier responses from requests.txt file.
for requests the script prints:
1. endpoint
2. method
3. the arguments from the request in a dictionary

for responses the script prints the payload, and in the case of JSON it parses it into a dictionary.

## Usage:
1. add requests and responses to requests.txt, by order of requests and responses after the requests with support for delay responses.
ex: req_(1),res_(1),req_(2),req_(3),res_(2),res_(3)
2. add CR-LF of 80 "-" at the end of each request or response
3. run by typing ```python service.py```

## requests.txt:
includes requests and responses from https://jsonplaceholder.typicode.com/ and requests from my personal honey-pot

## Output for requests.txt:
```bash
------------------------------http request------------------------------
Method: GET
endpoint: /typicode/demo/comments
arguments: {}
------------------------------http response------------------------------
response json payload :
[{u'body': u'some comment', u'postId': 1, u'id': 1}, {u'body': u'some comment', u'postId': 1, u'id': 2}]
------------------------------http request------------------------------
Method: GET
endpoint: /typicode/demo/comments
arguments: {}
------------------------------http response------------------------------
response json payload :
[{u'body': u'some comment', u'postId': 1, u'id': 1}, {u'body': u'some comment', u'postId': 1, u'id': 2}]
------------------------------http request------------------------------
Method: GET
endpoint: /typicode/demo/profile
arguments: {}
------------------------------http response------------------------------
response json payload :
{u'name': u'typicode'}
------------------------------http request------------------------------
Method: GET
endpoint: /typicode/demo/comments
arguments: {'id': '1'}
------------------------------http response------------------------------
response json payload :
[{u'body': u'some comment', u'postId': 1, u'id': 1}]
------------------------------http request------------------------------
Method: GET
endpoint: /
arguments: {'XDEBUG_SESSION_START': 'phpstorm'}
------------------------------http request------------------------------
Method: POST
endpoint: /boaform/admin/formLogin
arguments: {'username': 'admin', 'psd': 'Feefifofum'}
------------------------------http request------------------------------
Method: POST
endpoint: /api/jsonws/invoke
arguments: {u'test': u'testing...'}

```
