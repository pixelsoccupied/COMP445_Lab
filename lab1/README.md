COMP 445 Lab 1

### Setup

##### Basic setup
```shell
$ python httpc (get|post) [-v] (-hd "k:v")* [-d inline-data] [-f file] -u URL
```

##### Without extension and python prefix
```shell
$ chmod +x httpc
$ ./httpc (get|post) [-v] (-hd "k:v")* [-d inline-data] [-f file] -u URL
```

##### Using as a command
```shell
$ chmod +x httpc
$ cd /usr/bin
$ [sudo] ln -s path/to/httpc .
$ httpc (get|post) [-v] (-hd "k:v")* [-d inline-data] [-f file] -u URL
```

### Help & Examples

##### General
```
httpc help
httpc is a curl-like application but supports HTTP protocol only.
Usage:
 httpc command [arguments]
The commands are:
 get executes a HTTP GET request and prints the response.
 post executes a HTTP POST request and prints the response.
 help prints this screen.
Use "httpc help [command]" for more information about a command.
```

##### GET
```
httpc help get
usage: httpc get [-v] [-h key:value] URL
Get executes a HTTP GET request for a given URL.
 -v Prints the detail of the response such as protocol,
status, and headers.
 -h key:value Associates headers to HTTP Request with the format
'key:value'.
```

###### Example

`httpc get -hd Accept:application/json -v -u 'http://httpbin.org/get?course=networking&assignment=1%27'`

```
** Server Response **
HTTP/1.1 200 OK
Server: nginx
Date: Wed, 08 Feb 2017 22:59:21 GMT
Content-Type: application/json
Content-Length: 253
Connection: close
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true

{
  "args": {
    "assignment": "1'",
    "course": "networking"
  },
  "headers": {
    "Accept": "application/json",
    "Host": "httpbin.org"
  },
  "origin": "144.172.191.21",
  "url": "http://httpbin.org/get?course=networking&assignment=1'"
}
```


##### POST
```
httpc help post
usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL
Post executes a HTTP POST request for a given URL with inline data or
from file.
 -v Prints the detail of the response such as protocol, status, and headers.
 -h key:value Associates headers to HTTP Request with the format
'key:value'.
 -d string Associates an inline data to the body HTTP POST
request.
 -f file Associates the content of a file to the body HTTP
POST request.
Either [-d] or [-f] can be used but not both.
```

###### Example
`httpc post -hd Accept:application/json -v -d '{"test":"test"}' -u 'http://httpbin.org/post' -o 'output.txt'`

```
** Server Response **
HTTP/1.1 200 OK
Server: nginx
Date: Wed, 08 Feb 2017 23:00:45 GMT
Content-Type: application/json
Content-Length: 340
Connection: close
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true

{
  "args": {},
  "data": "{\"test\": \"test\"}",
  "files": {},
  "form": {},
  "headers": {
    "Accept": "application/json",
    "Content-Length": "16",
    "Content-Type": "application/json",
    "Host": "httpbin.org"
  },
  "json": {
    "test": "test"
  },
  "origin": "144.172.191.21",
  "url": "http://httpbin.org/post"
}
```
