#!/usr/bin/env python
# -*- coding: utf-8 -*-

import BaseHTTPServer
import codecs

class MyCustomHTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    data = {}

    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "File not found")
            return
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset: utf-8")
        self.end_headers()
        self.render_page()

    def render_page(self):
        with codecs.open("layout.html", encoding="utf-8") as layout_file:
            layout = layout_file.read()
            self.data["rendered_items"] = u""
            with codecs.open("item_template.html", encoding="utf-8") as item_template_file:
                item_template = item_template_file.read()
                for item in self.data["items"]:
                    self.data["rendered_items"] += item_template.format(**item)
            page = layout.format(**self.data).encode("utf-8")
            self.wfile.write(page)

def main(address, port, data):
    MyCustomHTTPHandler.data = data
    httpd = BaseHTTPServer.HTTPServer((address, port), MyCustomHTTPHandler)
    print "serving at port http://{0}:{1}".format(address, port)
    httpd.serve_forever()

if __name__ == "__main__":
    data = {
        "title": u"Learning C++ for beginners",
        "description": u"Learning to code In C++?  Here’s a few links where it will all help you get started.",
        "items": [
            {"title": u"MODULE ONE: “Choose a complier”", 
             "youtube_link": "https://www.youtube.com/watch?v=tvC1WCdV1XU", 
             "description": u"""Here will be between 1-5 sentences about the video discussing about on what the user
		should expect to know after watching it. Here will be between 1-5 sentences about  the video 
		discussing about on <i>what the user should expect to know after watching it</i>. <br />
		Here will be between 1-5 sentences   about the video discussing about on what the user
		should expect to know after watching it. <br />
        Here will be between 1-5 sentences about the video 
		discussing about on what the user should expect to know after watching it.
        """},
            {"title": u"MODULE TWO: “Hello World!”", 
             "youtube_link": "https://www.youtube.com/watch?v=SWZfFNyUsxc", 
             "description": u"""
             Here will be between 1-5 sentences about the video discussing about on what the user
		should expect to know after watching it. Here will be between 1-5 sentences about  the video 
		discussing about on what the user <code>python is cool</code> should expect to know after watching it. <br />
		Here will be between 1-5 sentences   about the video discussing about on what the user
		should expect <b>to know after watching it</b>. Here will be between 1-5 sentences about the video 
		discussing about on what the user should expect to know after watching it.
             """},    
        ]
    }
    main("0.0.0.0", 8080, data)