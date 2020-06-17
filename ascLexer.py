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
t_TVAR          = r'\$t(\d+)'
t_AVAR          = r'\$a(\d+)'
t_VVAR          = r'\$v(\d+)'
t_RVAR          = r'\$ra'
t_SVAR          = r'\$s(\d+)'
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
    t.lexer.lineno += len("\n")

def t_error(t):
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

from operation import ValExpression, OperationExpression
from expression import ValType, Operator
from instruction import Assignment, If, GoTo, Label, Print, Unset, Exit, RegisterType

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
    t[0] = [t[1],t[3]]

def p_ist_unJmp(t):
    '''ist  : GOTO LBS SCOLON'''
    gt = GoTo(t[2], t.lineno(1))
    t[0] = [gt]

def p_ist_cdJmp(t):
    '''ist  : IF PARIZQ opr PARDER GOTO LBS SCOLON'''
    cdJmp = If(t[3],t[6], t.lineno(1))
    t[0] = [cdJmp]

def p_ist_lbs(t):
    '''ist  : LBS COLON'''
    Lbl = Label(t[1], t.lineno(1))
    t[0] = [Lbl]

def p_ist_ntv(t):
    '''ist  : ntv SCOLON'''
    t[0] = [t[1]]

def p_empty(t):
    '''empty : '''
    pass

def p_ntv_unset(t):
    '''ntv  : UNSET PARIZQ idt PARDER'''
    t[0] = Unset(t[3], t.lineno(1))

def p_ntv_print(t):
    '''ntv  : PRINT PARIZQ opn PARDER'''
    t[0] = Print(t[3], t.lineno(1))

def p_ntv_exit(t):
    '''ntv  : EXIT'''
    t[0] = Exit()

def p_idt_dml(t):
    '''idt  : vrn dml'''
    asg_idt = t[1]
    asg_idt.valExp = t[2]
    t[0] = asg_idt

def p_idt(t):
    '''idt  : vrn '''
    t[0] = t[1]

def p_vrn_t(t):
    '''vrn  : TVAR'''
    idxVar = int(t[1][2:])
    t[0] = Assignment(idxVar, RegisterType.TVAR, None, t.lineno(1))

def p_vrn_a(t):
    '''vrn  : AVAR'''
    idxVar = int(t[1][2:])
    t[0] = Assignment(idxVar, RegisterType.AVAR, None, t.lineno(1))

def p_vrn_v(t):
    '''vrn  : VVAR'''
    idxVar = int(t[1][2:])
    t[0] = Assignment(idxVar, RegisterType.VVAR, None, t.lineno(1))

def p_vrn_r(t):
    '''vrn  : RVAR'''
    t[0] = Assignment(0, RegisterType.RVAR, None, t.lineno(1))

def p_vrn_s(t):
    '''vrn  : SVAR'''
    idxVar = int(t[1][2:])
    t[0] = Assignment(idxVar, RegisterType.SVAR, None, t.lineno(1))

def p_vrn_sp(t):
    '''vrn  : SPVAR'''
    t[0] = Assignment(0, RegisterType.SPVAR, None, t.lineno(1))

def p_dml1(t):
    '''dml  : dml dmn'''
    t[1].append(t[2])
    t[0] = t[1]

def p_dml2(t):
    '''dml  : dmn'''
    t[0] = [t[1]]

def p_dmn_int(t):
    '''dmn  : CORIZQ INT_VAL CORDER'''
    t[0] = t[2] #returns integer value

def p_dmn_string(t):
    '''dmn  : CORIZQ STRING_VAL CORDER'''
    t[0] = t[2] #returns string value

def p_dmn_idt(t):
    '''dmn  : CORIZQ vrn CORDER'''
    t[0] = t[2] #returns assignment instance

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
    if t[2] == '+':
        t[0] = OperationExpression(Operator.PLUS, t[1], t[3],t.lineno(1))
    elif t[2] == '-':
        t[0] = OperationExpression(Operator.MINUS, t[1], t[3] ,t.lineno(1))
    elif t[2] == '*':
        t[0] = OperationExpression(Operator.TIMES, t[1], t[3], t.lineno(1))
    elif t[2] == '/':
        t[0] = OperationExpression(Operator.QUOTIENT, t[1], t[3] ,t.lineno(1))
    elif t[2] == '%':
        t[0] = OperationExpression(Operator.REMAINDER, t[1], t[3],t.lineno(1))
    elif t[2] == '&&':
        t[0] = OperationExpression(Operator.AND, t[1], t[3] ,t.lineno(1))
    elif t[2] == 'xor':
        t[0] = OperationExpression(Operator.XOR, t[1], t[3] ,t.lineno(1))
    elif t[2] == '&':
        t[0] = OperationExpression(Operator.ANDBW, t[1], t[3] ,t.lineno(1))
    elif t[2] == '|':
        t[0] = OperationExpression(Operator.ORBW, t[1], t[3] ,t.lineno(1))
    elif t[2] == '^':
        t[0] = OperationExpression(Operator.XORBW, t[1], t[3] ,t.lineno(1))
    elif t[2] == '<<':
        t[0] = OperationExpression(Operator.SHL, t[1], t[3] ,t.lineno(1))
    elif t[2] == '>>':
        t[0] = OperationExpression(Operator.SHR, t[1], t[3] ,t.lineno(1))
    elif t[2] == '==':
        t[0] = OperationExpression(Operator.EQ, t[1], t[3] ,t.lineno(1))
    elif t[2] == '!=':
        t[0] = OperationExpression(Operator.NEQ, t[1], t[3] ,t.lineno(1))
    elif t[2] == '>':
        t[0] = OperationExpression(Operator.GR, t[1], t[3] ,t.lineno(1))
    elif t[2] == '>=':
        t[0] = OperationExpression(Operator.GRE, t[1], t[3] ,t.lineno(1))
    elif t[2] == '<':
        t[0] = OperationExpression(Operator.LS, t[1], t[3] ,t.lineno(1))
    elif t[2] == '<=':
        t[0] = OperationExpression(Operator.LSE, t[1], t[3] ,t.lineno(1))

def p_nopr(t):
    '''opr  : READ PARIZQ PARDER
            | ARRAY PARIZQ PARDER'''
    if t[1] == 'read':
        t[0] = OperationExpression(Operator.READ, None, None,t.lineno(1))
    elif t[1] == 'array':
        t[0] = OperationExpression(Operator.ARRAY, None, None,t.lineno(1))
            
def p_uopr(t):
    '''opr  : MINUS opn
            | NOT opn
            | NOTBW opn
            | ANDBW idt
            | ABS PARIZQ opn PARDER'''
    if t[1] == '-':
        t[0] = OperationExpression(Operator.NEGATIVE, t[2], None,t.lineno(1))
    elif t[1] == '!':
        t[0] = OperationExpression(Operator.NOT, t[2], None,t.lineno(1))
    elif t[1] == '~':
        t[0] = OperationExpression(Operator.NOTBW, t[2], None,t.lineno(1))
    elif t[1] == '&':
        t[0] = OperationExpression(Operator.AMP, ValExpression(t[2],ValType.REFVAR), None,t.lineno(1))
    elif t[1] == 'abs':
        t[0] = OperationExpression(Operator.ABS, t[3], None,t.lineno(1))

def p_copr(t):
    '''opr  : PARIZQ INT PARDER idt
            | PARIZQ FLOAT PARDER idt
            | PARIZQ CHAR PARDER idt'''
    if t[2] == 'int':
        t[0] = OperationExpression(Operator.CINT, ValExpression(t[4],ValType.REFVAR,t.lineno(1)), None,t.lineno(1))
    elif t[2] == 'float':
        t[0] = OperationExpression(Operator.CFLOAT, ValExpression(t[4],ValType.REFVAR,t.lineno(1)), None,t.lineno(1))
    elif t[2] == 'char':
        t[0] = OperationExpression(Operator.CCHAR, ValExpression(t[4],ValType.REFVAR,t.lineno(1)), None,t.lineno(1))

def p_opn_opr(t):
    '''opr  : opn'''
    t[0] = t[1]

def p_opnf(t):
    '''opn  : FLOAT_VAL'''
    t[0] = ValExpression(t[1],ValType.FLOAT,t.lineno(1))

def p_opni(t):
    '''opn  : INT_VAL'''
    t[0] = ValExpression(t[1],ValType.INTEGER,t.lineno(1))

def p_opns(t):
    '''opn  : STRING_VAL'''
    t[0] = ValExpression(t[1],ValType.STRING,t.lineno(1))

def p_opnr(t):
    '''opn  : idt'''
    #t[1] is an instance of Assignment
    t[0] = ValExpression(t[1],ValType.REFVAR,t.lineno(1))

def p_error(t):
    if t:
        parser.errok()

import ply.yacc as yacc
parser = yacc.yacc()

def parse(input):
    return parser.parse(input)