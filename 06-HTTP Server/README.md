# Introduction
The goal of this lab is to write a short Python program, to respond to HTTP requests and return web resources, acting as an HTTP server.

# Procedure
Download the skeleton Python template: http_server.py

Complete the handle_request method to parse a request and respond by returning the designated resource. You will want to add other helper methods, but do not change any other code provided in the template.

Note that this method will be invoked on a separate thread for each request received. This means that there may be multiple copies of this method running simultaneously, if the web client opens more than one connection at a time (e.g., to download resources that are referenced in a main HTML file).

For this reason, you should not rely on any global variables, but instead pass data as arguments to related functions. Each thread will have its own execution stack.

You may not use a prebuilt library like Lib/BaseHTTPServer; the point of this lab is for you to understand the low-level implementation of the HTTP protocol.

You should use the utility functions that are included near the end of the skeleton template file. Read the description for each function and ask the instructor if you have questions about them.

If this base functionality turns out to be too easy, you may experiment with adding additional functions, but be sure the basic requirements are still met.

# Assignment details
Your server is only expected to handle "file" resources, so that you can service a client request by returning the contents of a file associated with the resource identifier.

You must be able to serve at least the following resources. Download each of them from the table below:

| Relative URL | File path, relative to the directory with your Python server code file | File to serve (Open the file in by clicking the link to bring up a preview then click "Download ....") |
| :----: | :----: | :----: |
| / (default) | ./index.html | index.html |
| /index.html | ./index.html | index.html |
| /sebern1.jpg | ./sebern1.jpg | sebern1.jpg |
| /style.css |./style.css | style.css |
| /e-sebern2.gif | ./e-sebern2.gif | e-sebern2.gif |

While you do not need to serve any additional files, your server should be capable of serving additional files without altering the program's code.

Your server should work when you browse to http://localhost:8080

You must parse the request Request-Line and all request header lines, storing the key/value pairs from the headers in a Python dictionary.

Unless you implement additional functionality, it is unlikely that you will need to make use of any of the request headers, but you should store and print them after the entire request is received, so you can verify that you are handling the request correctly.
You do not need to print the headers in the same order they were received. The order the dictionary iterates them is fine.
You must return an appropriate response Status-Line and header lines to the requesting client, regardless of what the user types in the URL. You should send a body with the message if the RFC specifies that there should be one for the status code(s) you use.

Use a Python dictionary to store the response header lines, and then send them all at once at an appropriate time.

The response header lines must include: (again, in the order that a dictionary iterates is fine)

A Date header (in proper RFC format) indicating the time that the request was satisfied.

A Connection header indicating that a non-persistent connection will be used.

A Content-Type header with an appropriate MIME type (you should use the provided function to get the MIME type).

A Content-Length header to specify the size of the resource being returned (if there is one to return).
You are not required to use chunked encoding for any file type.
Optionally, you may use chunked encoding for text/html resources. If you do so, you must include the appropriate Transfer-Encoding header instead of Content-Length, and format the resource data appropriately in the response.

As in previous labs, write in comments at the beginning of your program

An Introduction, describing the lab in your own words, and
A Conclusion, describing what you learned, what you liked or disliked about the lab and any suggestions for improvement.
Also as before, you should not use HTTP libraries when implementing this lab.

# Hints and Notes
To test your code, direct your browser to localhost:8080
As in the HTTP client lab, you will have to both send and receive on the TCP connection to the HTTP client. On the receiving side, since we will only be handling GET requests with no entity bodies, there will likely be only one kind of data that needs to be processed: "Textual" data, organized as a sequence of ASCII characters followed by the CR/LF pair. Data in this category includes:

The HTTP Request-Line.
Request header lines.
"Blank" lines (e.g., to terminate a header). You should probably have a "read line" function from the HTTP client lab, which you can likely use here.

Remember that when you read from the network stream with a function like recv, or from a file with a function like read, you can only control the maximum number of bytes that will be returned. You will always get at least one byte, unless there is no more data (in the case of a file or a socket that has been closed), but there is no way to predict absolutely in advance how many bytes will be available when you make the recv or read call.

At times, you may get fewer than the number of bytes needed (e.g., in a block of "binary byte" data). If this happens, you will have to make another recv call to get additional data. If you choose to send a chunked file, you may choose to send whatever recv gives you immediately, instead of calling it again. This might reduce the latency of your response.

When serving resource data from a file, open the file in binary ('rb') mode to avoid problems with line-ending modification on Windows.

Getting the proper HTTP "Date" value can be a little tricky. You can try something like this:
timestamp = datetime.datetime.utcnow()
timestring = timestamp.strftime('%a, %d %b %Y %H:%M:%S GMT')
 				#Sun, 06 Nov 1994 08:49:37 GMT

# Excellent Credit
There is one point allocated for "excellent credit" activities beyond the requirements. A couple of things that would work well might be implementing persistent connections or implementing caching. You could also implement file uploads by allowing the POST action in addition to the GET action. Check the RFC for additional features. Be sure to incorporate these cleanly into the request and response header dictionaries used in your design.

If you choose to implement the POST action, please ask, and I can help you set up a page that will allow your browser to generate a POST upload. (HTML is beyond the scope of this class.)

If you decide to implement a persistent connection, you can demonstrate that it is working by capturing the request in Wireshark.

Getting the excellent credit point is a challenge. If I see that you've made an effort, I'll want to give you the point, but I am reserving it for those teams which truly go above and beyond the requirements, demonstrating excellence in their extra work.

When you have questions you can't resolve, consult the instructor as soon as possible, in person or by email.

(Acknowledgements: The original version of this lab written by Dr. Sebern.)