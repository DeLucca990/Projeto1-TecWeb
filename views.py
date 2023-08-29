from urllib.parse import unquote_plus
from utils import load_template, build_response
from database import Database, Note
from html import escape

db = Database('./data/banco_projeto')

def edit(request):
    request = request.replace('\r', '') 
    partes = request.split('\n\n')
    corpo = partes[1]
    note_id = corpo.split('=')[1]
    note = db.get_id(note_id)
    return build_response(body=load_template('components/edit.html').format(id=note.id, title=note.title, content=note.content))

def update(request):
    request = request.replace('\r', '')
    partes = request.split('\n\n')
    corpo = partes[1]
    note_id = unquote_plus(corpo.split('&')[0]).split('=')[1]
    title = unquote_plus(corpo.split('&')[1].split('=')[1]).replace('+', ' ')
    content = unquote_plus(corpo.split('&')[2].split('=')[1]).replace('+', ' ')
    db.update(Note(id=note_id, title=title, content=content))
    return build_response(code=303, reason='See Other', headers='Location: /')

def delete(request):
    request = request.replace('\r', '')
    partes = request.split('\n\n')
    corpo = partes[1]
    note_id = corpo.split('=')[1]
    db.delete(note_id)
    return build_response(code=303, headers='Location: /')

def not_found(request):
    return build_response(code=404, reason='Not Found', body=load_template('error.html'))

def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for chave_valor in corpo.split('&'):
            # AQUI É COM VOCÊ
            chave, valor = chave_valor.split('=')
            params[unquote_plus(chave)] = unquote_plus(valor)
        titulo = params.get('titulo', '')
        detalhes = params.get('detalhes', '')
        db.add(Note(title=titulo, content=detalhes))
        
        return build_response(code=303, reason='See Other', headers='Location: /')

    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(id=note.id,title=escape(note.title), details=escape(note.content))
        for note in db.get_all()
    ]
    notes = '\n'.join(notes_li)
    response_body = load_template('index.html').format(notes=notes)
    return build_response(body=response_body)