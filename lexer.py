# lexer.py
import re

# Define token types
tokens = [
    'ID', 'PLUS', 'MULT', 'LPAREN', 'RPAREN'
]

# Regular expressions for tokens
token_specification = [
    ('PLUS', r'\+'),
    ('MULT', r'\*'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('ID', r'[0-9a-zA-Z]'),
    ('SKIP', r'[ \t]'),   # skip spaces/tabs
    ('MISMATCH', r'.'),   # any other character
]

# Compile regex
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
get_token = re.compile(tok_regex).match

def lex(characters):
    pos = 0
    line = characters
    tokens_list = []
    symbol_table = []
    mo = get_token(line)
    while mo is not None:
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'ID':
            tokens_list.append(('ID', value))
            symbol_table.append({'lexeme': value, 'token': 'ID'})
        elif kind == 'PLUS':
            tokens_list.append(('PLUS', value))
        elif kind == 'MULT':
            tokens_list.append(('MULT', value))
        elif kind == 'LPAREN':
            tokens_list.append(('LPAREN', value))
        elif kind == 'RPAREN':
            tokens_list.append(('RPAREN', value))
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character {value!r}')
        pos = mo.end()
        mo = get_token(line, pos)
    return tokens_list, symbol_table
