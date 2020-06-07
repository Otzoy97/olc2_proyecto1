reservedWords = {
    'if' : 'IF',
    'goto' : 'GOTO',

    'read' : 'READ',
    'array' : 'ARRAY',
    'unset' : 'UNSET',
    'print' : 'PRINT',
    'exit' : 'EXIT',

    'abs' : 'ABS',
    'xor' : 'XOR',

    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',

    'rvar' : 'RVAR'
}

tokens = [
    'TVAR',
    'AVAR',
    'VVAR',
    'RVAR',
    'SVAR',
    'SPVAR',
    'FLOAT_VAL',
    'INT_VAL',
    'STRING_VAL',
    'CORIZQ',
    'CORDER',
    'PARDER',
    'PARIZQ',
    'SCOLON',
    'COLON',
    'MINUS',
    'PLUS',
    'TIMES',
    'QUOTIENT',
    'REMAINDER',
    'NOT',
    'AND',
    'OR',
    'NOTBW',
    'ANDBW',
    'ORBW',
    'XORBW',
    'SHL',
    'SHR',
    'EQ',
    'ASSIGN',
    'NEQ',
    'GR',
    'GRE',
    'LS',
    'LSE',
    'LBS'
] + list(reservedWords.values())

t_CORIZQ        = r'\['
t_CORDER        = r'\]'
t_PARDER        = r'\)'
t_PARIZQ        = r'\('
t_SCOLON        = r';'
t_COLON         = r':'
t_PLUS          = r'-'
t_PLUS          = r'\+'
t_TIMES         = r'\*'
t_QUOTIENT      = r'/'
t_REMAINDER     = r'%'
t_NOT           = r'!'
t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOTBW         = r'~'
t_ANDBW         = r'&'
t_ORBW          = r'\|'
t_XORBW         = r'\^'
t_SHL           = r'<<'
t_SHR           = r'>>'
t_EQ            = r'=='
t_ASSIGN        = r'='
t_NEQ           = r'!='
t_GR            = r'>'
t_GRE           = r'>='
t_LS            = r'<'
t_LSE           = r'<='

def t_TVAR(t):
    r'\$t\d+'
    pass

def t_AVAR(t):
    r'\$a\d+'
    pass

def t_VVAR(t):
    r'\$v\d+'
    pass

def t_SVAR(t):
    r'\$s\d+'
    pass

def t_FLOAT_VAL(t):
    r'\d+\.\d+'
    pass

def t_INT_VAL(t):
    r'\d+'
    pass

def t_STRING_VAL(t):
    r'[\"][^\"\n]*[\"]'
    pass

def t_LBS(t):
    r'\w*'
    t.type = reservedWords.get(t.value.lower(), 'LBS')
    pass

def t_COMMENT(t):
    r'#[^\n]'

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print ("Illegal character '%s" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()