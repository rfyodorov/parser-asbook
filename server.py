#!/usr/bin/python
# -*- coding: utf-8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
from parser import *

PORT_NUMBER = 8000

class myHandler(BaseHTTPRequestHandler):
	
    #Handler for the GET requests
    def do_GET(self):
        if self.path[1:].isdigit():
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(getPage(self.path[1:]))

        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(getPage(1))

        try:
            #Check the file extension required and
	    #set the right mime type
	    sendReply = False
            if self.path.endswith(".html"):
	        mimetype='text/html'
	        sendReply = True
	    if self.path.endswith(".jpg"):
	        mimetype='image/jpg'
	        sendReply = True
	    if self.path.endswith(".gif"):
	        mimetype='image/gif'
	        sendReply = True
	    if self.path.endswith(".js"):
	        mimetype='application/javascript'
	        sendReply = True
	    if self.path.endswith(".css"):
	        mimetype='text/css'
	        sendReply = True

	    if sendReply == True:
	         #Open the static file requested and send it
                 f = open(curdir + sep + self.path) 
	         self.send_response(200)
	         self.send_header('Content-type',mimetype)
	         self.end_headers()
	         self.wfile.write(f.read())
	         f.close()
	    return
         
         
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()