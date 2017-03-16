COMP 445 Lab 2

### Setup

##### Basic setup
```shell
$ python httpfs [-v] [-p PORT] [-d PATH-TO-DIR]
```

##### Without extension and python prefix
```shell
$ chmod +x httpfs
$ ./httpfs [-v] [-p PORT] [-d PATH-TO-DIR]
```

##### Using as a command
```shell
$ chmod +x httpfs
$ cd /usr/bin
$ [sudo] ln -s path/to/httpfs .
$ httpfs [-v] [-p PORT] [-d PATH-TO-DIR]
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

##### Usage
```
httpfs is a simple file server.
usage: httpfs [-v] [-p PORT] [-d PATH-TO-DIR]
 -v Prints debugging messages.
 -p Specifies the port number that the server will listen and serve at. Default is 8080.
 -d Specifies the directory that the server will use to read/write
requested files. Default is the current directory when launching the
application.
```

###### Example

`httpfs -v -p 8080 -d '/path/to/dir'`
