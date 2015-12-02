#!/usr/bin/env python
# -*- coding: utf-8 -*-

import BaseHTTPServer
import codecs
import items

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
    #using data varible imported from items file
    main("0.0.0.0", 8080, items.data)
