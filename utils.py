import json
import os

def extract_route(string):
    return string.split()[1][1:] if len(string.split()) > 1 else ''

def read_file(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        return content

def load_data(filename):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'data', filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def load_template(filename):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'desafio-css', filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    return data

def add_note(new_note):
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'notes.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        notes = json.load(file)
    notes.append(new_note)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(notes, file, indent=4)

def build_response(body='', code=200, reason='OK', headers=''):
    status_line = f'HTTP/1.1 {code} {reason}\n'
    response_headers = headers if headers else 'Content-Type: text/html\n'
    
    response = f'{status_line}{response_headers}\n{body}'
    
    return response.encode()
    