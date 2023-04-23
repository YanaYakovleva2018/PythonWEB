from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import json
import logging
import mimetypes
import pathlib
import socket
import urllib.parse

BASE_DIR = pathlib.Path()

def send_to_socket(data):
    cli_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cli_socket.sendto(data, ('127.0.0.1', 5000))
    cli_socket.close()


class HttpHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        send_to_socket(data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        parse_url = urllib.parse.urlparse(self.path)
        if parse_url.path == '/':
            self.send_html_file('index.html')
        elif parse_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(parse_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def run_http_server(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('0.0.0.0', 3000)
    http = server_class(server_address, handler_class)
    logging.info('Http server started')
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

def run_socket_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    server_socket.bind(server)
    logging.info('Socket server started')
    try:
        while True:
            data, address = server_socket.recvfrom(1024)
            save_data(data)
    except KeyboardInterrupt:
        logging.info('Destroy server')
    finally:
        server_socket.close()

def save_data(data):
    data_parse = urllib.parse.unquote_plus(data.decode())
    try:
        data_dict = {str(datetime.now()): {key: value for key, value in [i.split('=') for i in data_parse.split('&')]}}

        with open(BASE_DIR.joinpath('storage/data.json'), 'r+', encoding='utf-8') as fd:
            try:
                data_file = json.load(fd)
            except:
                data_file = {}
            data_file.update(data_dict)
            fd.seek(0)
            json.dump(data_file, fd, ensure_ascii=False, indent=4)
            fd.truncate()
    except ValueError as err:
        logging.error(f'For data {data_parse} error {err}')
    except OSError as err:
        logging.error(f'Write data {data_parse} error {err}')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(threadName)s %(message)s')
    
    STORAGE_DIR = pathlib.Path().joinpath('storage')
    FILE_STORAGE = STORAGE_DIR / 'data.json'
    if not FILE_STORAGE.exists():
        with open(FILE_STORAGE, 'w', encoding='utf-8') as fd:
            json.dump({}, fd, ensure_ascii=False)

    thread_server = Thread(target=run_http_server)
    thread_server.start()
    
    thread_socket = Thread(target=run_socket_server('127.0.0.1', 5000))
    thread_socket.start()
