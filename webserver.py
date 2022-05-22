import http.server
import socketserver
import cgi
import json
PORT = 8079
import audiorec
import io

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "Hier is niks te zien"
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        r, info = self.deal_post_data()
        print('task:',info)
        message = 'x'
        if info == 'add' or info == 'new' or info == 'match':
          
            try:
                message = {'status': 'succes'}
                message['result'] = audiorec.main(info)
            except:
                message = {'status':'error'}
            print(message)
            #message['status'] = 'succes'


        self._set_headers()
        self.wfile.write(bytes(json.dumps(message), "utf8"))


    def deal_post_data(self):
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
        if ctype == 'multipart/form-data':
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'], })
            dict = {}
            for y in form:
                if y != 'file':
                    dict[str(y)] = form[y].value

            #return dict['task']
            try:
                if isinstance(form["file"], list):
                    for record in form["file"]:
                        open("/home/joey/audfprint-master/%s" % record.filename, "wb").write(record.file.read())
                else:
                    open("/home/joey/audfprint-master/%s" % form["file"].filename, "wb").write(form["file"].file.read())
            except IOError:
                return (False, "Can't create file to write, do you have permission to write?")
        return (True,dict['task'])

Handler = CustomHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
