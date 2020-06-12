class AscNode:
    def __init__(self, val):
        self.val = val
        self.children = []

    def add(self, node):
        self.children.append(node)

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
    'char' : 'CHAR'
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
t_MINUS          = r'-'
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
t_TVAR          = r'\$t\d+'
t_AVAR          = r'\$a\d+'
t_VVAR          = r'\$v\d+'
t_RVAR          = r'\$ra'
t_SVAR          = r'\$s\d+'
t_SPVAR          = r'\$sp'

def t_FLOAT_VAL(t):
    r'(\+|-)?\d+\.\d+'
    try:
        t.value = float(t.value)
    except:
        t.value = 0.0
    return t

def t_INT_VAL(t):
    r'(\+|-)?\d+'
    try:
        t.value = int(t.value)
    except:
        t.value = 0
    return t

def t_STRING_VAL(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t

def t_LBS(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservedWords.get(t.value.lower(), 'LBS')
    return t

def t_COMMENT(t):
    r'\#.*\n'
    t.lexer.lineno += 1

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    #print ("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

def p_init(t):
    '''init  : list '''
    t[0] = t[1]

def p_init1(t):
    '''init : empty '''
    pass

def p_list2(t):
    '''list : ist'''
    t[0] = [t[1]]

def p_list1(t):
    '''list : list ist'''
    t[1].append(t[2])
    t[0] = t[1]

def p_ist_assign(t):
    '''ist  : idt ASSIGN opr SCOLON'''
    t[0] = AscNode('Assign')
    t[0].add(t[1])
    t[0].add(t[3])

def p_ist_unJmp(t):
    '''ist  : GOTO LBS SCOLON'''
    t[0] = AscNode('Goto')
    r = AscNode(t[2])
    t[0].add(r)

def p_ist_cdJmp(t):
    '''ist  : IF PARIZQ opr PARDER GOTO LBS SCOLON'''
    t[0] = AscNode('If')
    t[0].add(t[3])
    t[0].add(AscNode(t[6]))

def p_ist_lbs(t):
    '''ist  : LBS COLON'''
    t[0] = AscNode('Label')
    r = AscNode(t[1])
    t[0].add(r)

def p_ist_ntv(t):
    '''ist  : ntv SCOLON'''
    t[0] = t[1]

def p_empty(t):
    '''empty : '''
    pass

def p_ntv_unset(t):
    '''ntv  : UNSET PARIZQ idt PARDER'''
    t[0] = AscNode('Unset')
    t[0].add(t[3])

def p_ntv_print(t):
    '''ntv  : PRINT PARIZQ opn PARDER'''
    t[0] = AscNode('Print')
    t[0].add(t[3])

def p_ntv_exit(t):
    '''ntv  : EXIT'''
    t[0] = AscNode('Exit')

def p_idt_dml(t):
    '''idt  : vrn dml'''
    t[0] = t[1]
    for i in t[2]:
        t[0].add(i)

def p_idt(t):
    '''idt  : vrn '''
    t[0] = t[1]

def p_vrn(t):
    '''vrn  : TVAR 
    | AVAR 
    | VVAR 
    | SVAR 
    | SPVAR 
    | RVAR'''
    t[0] = AscNode(t[1])

def p_dml1(t):
    '''dml  : dml dmn'''
    t[1].append(t[2])
    t[0] = t[1]

def p_dml2(t):
    '''dml  : dmn'''
    t[0] = [t[1]]

def p_dmn_int(t):
    '''dmn  : CORIZQ INT_VAL CORDER 
    | CORIZQ STRING_VAL CORDER'''
    t[0] = AscNode(t[2])

def p_dmn_idt(t):
    '''dmn  : CORIZQ vrn CORDER'''
    t[0] = t[2]

def p_bopr(t):
    '''opr : opn PLUS opn
            | opn MINUS opn
            | opn TIMES opn
            | opn QUOTIENT opn
            | opn REMAINDER opn
            | opn AND opn
            | opn XOR opn
            | opn OR opn
            | opn ANDBW opn
            | opn ORBW opn
            | opn XORBW opn
            | opn SHL opn
            | opn SHR opn
            | opn EQ opn
            | opn NEQ opn
            | opn GR opn
            | opn GRE opn
            | opn LS opn
            | opn LSE opn'''
    r = AscNode(t[2])
    r.add(t[1])
    r.add(t[3])
    t[0] = r

def p_nopr(t):
    '''opr  : READ PARIZQ PARDER
            | ARRAY PARIZQ PARDER'''
    t[0] = AscNode(t[1])
            
def p_uopr(t):
    '''opr  : MINUS opn
            | NOT opn
            | NOTBW opn
            | ANDBW idt
            | ABS PARIZQ opn PARDER'''
    r = AscNode(t[1])
    if t[1] == 'abs':
        r.add(t[3])
    else:
        r.add(t[2])
    t[0] = r


def p_copr(t):
    '''opr  : PARIZQ INT PARDER idt
            | PARIZQ FLOAT PARDER idt
            | PARIZQ CHAR PARDER idt'''
    r = AscNode(t[2])
    r.add(t[4])
    t[0] = r

def p_opn_opr(t):
    '''opr  : opn'''
    t[0] = t[1]

def p_opnf(t):
    '''opn  : FLOAT_VAL 
    | INT_VAL 
    | STRING_VAL'''
    t[0] = AscNode(t[1])

def p_opnr(t):
    '''opn  : idt'''
    t[0] = t[1]

def p_error(t):
    #print(t)
    pass

import ply.yacc as y
from graphviz import Digraph
from datetime import datetime

parser = y.yacc()
dot = Digraph(comment='ascAST')

def createAST(input):
    '''
        Construct an ast tree from the root that the parser return
    '''
    lexer.lineno = 1
    root = parser.parse(input)
    if root:
        # if root is not None
        dot.node(str(id(root)),'S')
        for i in root:
            dot.node(str(id(i)), str(i.val))
            dot.edge(str(id(root)), str(id(i)))
            travelTree(i)
    #print(dot.source)
    #retrieve actual date and time
    now = datetime.now()
    fstr = now.strftime("%d%m%y-%H%M%S")
    #render the graph
    dot.render('ascAST'+fstr,'report',False,True,'png')
    #clear the stack parser
    parser.restart()
    #clear the dot body
    dot.clear()

def travelTree(root):
    '''
        Recursively goes through the nodes and construct an ast tree
    '''
    for i in root.children:
        dot.node(str(id(i)), str(i.val))
        dot.edge(str(id(root)), str(id(i)))
        travelTree(i)


