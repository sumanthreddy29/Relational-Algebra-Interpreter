import ply.lex as lex

reserved = {
  'project': 'PROJECT',
  'select': 'SELECT',
  'rename': 'RENAME',
  'union': 'UNION',
  'times': 'TIMES',
  'minus': 'MINUS',
  'intersect': 'INTERSECT',
  'join': 'JOIN',
  'and': 'AND'
}

tokens = ['SEMICOLON','LPAREN','RPAREN','SLPAREN','SRPAREN','STRING','COMPARISON','COMMA','NAME','NUMBER'] + list(reserved.values())

t_SEMICOLON= r'\;'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SLPAREN = r'\['
t_SRPAREN = r'\]'
t_STRING=r'[\'][^\'\n]*[\']'
t_COMPARISON= r'<> |= | >= | <= | < | >' 
t_COMMA=r','

def t_NAME(t):
  r'[a-zA-Z][a-zA-Z0-9_]*'
  t.type = reserved.get(t.value.lower(),'NAME')
  return t

def t_NUMBER(t):
    r'[0-9]+ | [0-9]+"."[0-9]* | "."[0-9]*'
    t.value = int(t.value)
    return t

# Ignored characters
t_ignore = " \r\n\t"
t_ignore_COMMENT = r'\#.*'

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

lexer = lex.lex()

## Test it out
#data = '''
#select[A = 10 and B > C](employee join department)
#'''
#
## Give the lexer some input
#lexer.input(data)
##
## Tokenize
#while True:
#  tok = lexer.token()
#  if not tok: 
#    break      # No more input
#  print(tok)
