from enum import Enum

class Operator(Enum):
    '''All operators'''
    PLUS = 1        # +
    MINUS = 2       # -
    TIMES = 3       # *
    QUOTIENT = 4    # /
    REMAINDER = 5   # %
    NEGATIVE = 6    # -
    ABS = 7         # abs
    NOT = 8         # !
    AND = 9         # &&
    XOR = 10        # xor
    OR = 11         # ||
    NOTBW = 12      # ~ 
    ANDBW = 13      # &
    ORBW = 14       # |
    XORBW = 15      # ^
    SHL = 16        # <<
    SHR = 17        # >>
    EQ = 18         # =
    NEQ = 19        # !=
    GR = 20         # >
    GRE = 21        # >=
    LS = 22         # <
    LSE = 23        # <=
    AMP = 24        # &
    CINT = 25       # int
    CFLOAT = 26     # float
    CSTRING = 27    # string
    READ = 28       # read()
    ARRAY = 29      # array()

class ValType(Enum):
    '''Supported types'''
    CHAR = 1
    STRING = 2
    FLOAT = 3
    INTEGER = 4
    POINTER = 5
    ARRAY = 6
    STRUCT = 7

class Expression:
    '''
        Abstract class for expressions
    '''

class ValExpression(Expression):
    '''
    '''
    def __init__(self, value, type):
        self.value = value
        self.type = type

class ReadExpression(Expression):
    '''
    '''

class OperationExpression(Expression):
    '''
    '''
    def __init__(self, op, e1, e2 = None):
        self.e1 = e1
        self.e2 = e2
        self.op = op 