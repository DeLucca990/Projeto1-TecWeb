import os

def extract_route(string):
    return string.split()[1][1:] if len(string.split()) > 1 else ''

def read_file(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        return content

def load_template(filename):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'desafio-css', filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    return data

def build_response(body='', code=200, reason='OK', headers=''):
    status_line = f'HTTP/1.1 {code} {reason}\n'
    response_headers = headers if headers else 'Content-Type: text/html\n'
    
    response = f'{status_line}{response_headers}\n{body}'
    
    return response.encode()
    