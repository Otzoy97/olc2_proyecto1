from expression import *
from instruction import *

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
        t[0] = OperationExpression(Operator.PLUS, t[1], t[3] )
    elif t[2] == '-':
        t[0] = OperationExpression(Operator.MINUS, t[1], t[3] )
    elif t[2] == '*':
        t[0] = OperationExpression(Operator.TIMES, t[1], t[3] )
    elif t[2] == '/':
        t[0] = OperationExpression(Operator.QUOTIENT, t[1], t[3] )
    elif t[2] == '%':
        t[0] = OperationExpression(Operator.REMAINDER, t[1], t[3] )
    elif t[2] == '&&':
        t[0] = OperationExpression(Operator.AND, t[1], t[3] )
    elif t[2] == 'xor':
        t[0] = OperationExpression(Operator.XOR, t[1], t[3] )
    elif t[2] == '&':
        t[0] = OperationExpression(Operator.ANDBW, t[1], t[3] )
    elif t[2] == '|':
        t[0] = OperationExpression(Operator.ORBW, t[1], t[3] )
    elif t[2] == '^':
        t[0] = OperationExpression(Operator.XORBW, t[1], t[3] )
    elif t[2] == '<<':
        t[0] = OperationExpression(Operator.SHL, t[1], t[3] )
    elif t[2] == '>>':
        t[0] = OperationExpression(Operator.SHR, t[1], t[3] )
    elif t[2] == '==':
        t[0] = OperationExpression(Operator.EQ, t[1], t[3] )
    elif t[2] == '!=':
        t[0] = OperationExpression(Operator.NEQ, t[1], t[3] )
    elif t[2] == '>':
        t[0] = OperationExpression(Operator.GR, t[1], t[3] )
    elif t[2] == '>=':
        t[0] = OperationExpression(Operator.GRE, t[1], t[3] )
    elif t[2] == '<':
        t[0] = OperationExpression(Operator.LS, t[1], t[3] )
    elif t[2] == '<=':
        t[0] = OperationExpression(Operator.LSE, t[1], t[3] )

def p_nopr(t):
    '''opr  : READ PARIZQ PARDER
            | ARRAY PARIZQ PARDER'''
    if t[1] == 'read':
        t[0] = OperationExpression(Operator.READ)
    elif t[1] == 'array':
        # TODO: indicate de value to store something like a dictionary
        t[0] = OperationExpression(Operator.ARRAY)
            
def p_uopr(t):
    '''opr  : MINUS opn
            | NOT opn
            | NOTBW opn
            | ANDBW idt'''
    if t[1] == '-':
        t[0] = OperationExpression(Operator.MINUS, t[2])
    elif t[1] == '!':
        t[0] = OperationExpression(Operator.NOT, t[2])
    elif t[1] == '~':
        t[0] = OperationExpression(Operator.NOTBW, t[2])
    elif t[1] == '&':
        t[0] = OperationExpression(Operator.AMP, t[2])
            
def p_copr(t):
    '''opr  : PARIZQ INT PARDER idt
            | PARIZQ FLOAT PARDER idt
            | PARIZQ CHAR PARDER idt'''
    if t[2] == 'int':
        t[0] = OperationExpression(Operator.CINT, t[4])
    elif t[2] == 'float':
        t[0] = OperationExpression(Operator.CFLOAT, t[4])
    elif t[2] == 'char':
        t[0] = OperationExpression(Operator.CCHAR, t[4])
            