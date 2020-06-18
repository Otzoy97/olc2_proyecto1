from ascAST import AscNode
from err import addErr, ErrType

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
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except:
        t.value = 0.0
    return t

def t_INT_VAL(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except:
        t.value = 0
    return t

def t_STRING_VAL(t):
    r'\".*?\"|\'.*?\''
    t.value = t.value[1:-1]
    return t

def t_LBS(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservedWords.get(t.value.lower(), 'LBS')
    return t

def t_COMMENT(t):
    r'\#.*\n*?'
    t.lexer.lineno += 1

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    addErr(ErrType.LEXIC, 'Illegal character: ' + str(t.value[0]), t.lexer.lineno)
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

def p_list1(t):
    '''list : ist list_p'''
    t[2].insert(0,t[1])
    t[0] = t[2]

def p_list2(t):
    '''list_p : ist list_p'''
    t[2].insert(0,t[1])
    t[0] = t[2]

def p_list3(t):
    '''list_p : empty'''
    t[0] = []

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

def p_idt(t):
    '''idt  : vrn fvrn'''
    t[0] = t[1]
    for i in t[2]:
        t[0].add(i)

def p_idt_Fdml1(t):
    '''fvrn  : dml'''
    t[0] = t[1]

def p_idt_Fdml2(t):
    '''fvrn  : empty'''
    t[0] = []

def p_vrn(t):
    '''vrn  : TVAR 
    | AVAR 
    | VVAR 
    | SVAR 
    | SPVAR 
    | RVAR'''
    t[0] = AscNode(t[1])

def p_dml1(t):
    '''dml  : dmn dml_p'''
    t[2].insert(0, t[1])
    t[0] = t[2]

def p_dml2(t):
    '''dml_p  : dmn dml_p'''
    t[2].insert(0, t[1])
    t[0] = t[2]

def p_dml3(t):
    '''dml_p  : empty'''
    t[0] = []

def p_dmn1(t):
    '''dmn  : CORIZQ fcorizq'''
    t[0] = t[2]

def p_dmn2(t):
    '''fcorizq  : INT_VAL CORDER 
    |  STRING_VAL CORDER'''
    t[0] = AscNode(t[1])


def p_dmn_idt(t):
    '''fcorizq  :  vrn CORDER'''
    t[0] = t[1]

def p_opr1(t):
    '''opr : opn fopn'''
    t[0] = t[2]

def p_opr2(t):
    '''opr : READ PARIZQ PARDER
    | ARRAY PARIZQ PARDER'''
    t[0] = AscNode(t[1])

def p_opr3(t):
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

def p_opr4(t):
    '''opr : PARIZQ fparizq'''
    t[0] = t[1]

def p_fopn1(t):
    '''fopn : PLUS opn
    | MINUS opn
    | TIMES opn
    | QUOTIENT opn
    | REMAINDER opn
    | AND opn
    | XOR opn
    | OR opn
    | ANDBW opn
    | ORBW opn
    | XORBW opn
    | SHL opn
    | SHR opn
    | EQ opn
    | NEQ opn
    | GR opn
    | GRE opn
    | LS opn
    | LSE opn'''
    r = AscNode(t[1])
    r.add(t[-1])
    r.add(t[2])
    t[0] = r

def p_fopn2(t):
    '''fopn : empty'''
    t[0] = t[-1]

def p_copr(t):
    '''fparizq  : INT PARDER idt
            | FLOAT PARDER idt
            | CHAR PARDER idt'''
    r = AscNode(t[1])
    r.add(t[3])
    t[0] = r

def p_opnf(t):
    '''opn  : FLOAT_VAL 
    | INT_VAL 
    | STRING_VAL'''
    t[0] = AscNode(t[1])

def p_opnr(t):
    '''opn  : idt'''
    t[0] = t[1]

def p_error(t):
    if t:
        tmp = str(t.value)
        if t.value == '>':
            tmp = "greater-than symbol"
        elif t.value == '<':
            tmp = "less-than symbol"
        addErr(ErrType.SINTACTIC, "Can't reduce '"+ tmp +"'", t.lineno)
        parser.errok()
    else:
        addErr(ErrType.SINTACTIC, "Unexpected EOF", "")

import ply.yacc as y
from graphviz import Digraph
from datetime import datetime

parser = y.yacc()
dot = Digraph(name='descAST')

def createASTD(input):
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
    dot.render('descAST'+fstr,'report',False,True,'pdf')
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
